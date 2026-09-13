import json
import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path


class BackupManager:
    FORMAT_VERSION = 1

    def __init__(
        self,
        vocabulary_database_path="database/vocabulary.json",
        settings_path="database/settings.json",
        image_directory="data/images",
        backup_directory="database/backups"
    ):
        self.vocabulary_database_path = Path(vocabulary_database_path)
        self.settings_path = Path(settings_path)
        self.image_directory = Path(image_directory)
        self.backup_directory = Path(backup_directory)

    def export_backup(self, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        vocabulary = self._read_json(
            self.vocabulary_database_path,
            []
        )
        settings = self._read_json(
            self.settings_path,
            {"visible_fields": [], "practice_ids": []}
        )
        deleted = self._read_json(
            self.vocabulary_database_path.parent / "deleted.json",
            {}
        )

        image_files = []
        if self.image_directory.exists():
            image_files = [
                p for p in self.image_directory.iterdir()
                if p.is_file()
            ]

        manifest = {
            "app": "FrenchFlashcard",
            "format_version": self.FORMAT_VERSION,
            "exported_at": datetime.now().astimezone().isoformat(),
            "vocabulary_count": len(vocabulary),
            "image_count": len(image_files),
            "deleted_count": len(deleted)
        }

        with zipfile.ZipFile(
            output_path,
            "w",
            compression=zipfile.ZIP_DEFLATED
        ) as archive:
            archive.writestr(
                "manifest.json",
                json.dumps(manifest, ensure_ascii=False, indent=4)
            )
            archive.writestr(
                "vocabulary.json",
                json.dumps(vocabulary, ensure_ascii=False, indent=4)
            )
            archive.writestr(
                "settings.json",
                json.dumps(settings, ensure_ascii=False, indent=4)
            )
            archive.writestr(
                "deleted.json",
                json.dumps(deleted, ensure_ascii=False, indent=4)
            )

            for image_path in image_files:
                archive.write(
                    image_path,
                    arcname=f"images/{image_path.name}"
                )

        return output_path

    def import_backup(self, backup_path, manager, settings):
        backup_path = Path(backup_path)

        with tempfile.TemporaryDirectory(prefix="FrenchFlashcard_import_") as temp_dir:
            temp_dir = Path(temp_dir)
            self._safe_extract(backup_path, temp_dir)

            manifest = self._read_json(temp_dir / "manifest.json", None)
            if not manifest:
                raise ValueError("Invalid backup: manifest.json is missing.")

            if manifest.get("app") != "FrenchFlashcard":
                raise ValueError("This ZIP is not a FrenchFlashcard backup.")

            if manifest.get("format_version") != self.FORMAT_VERSION:
                raise ValueError(
                    f"Unsupported backup format version: "
                    f"{manifest.get('format_version')}"
                )

            incoming = self._read_json(temp_dir / "vocabulary.json", [])
            incoming_settings = self._read_json(
                temp_dir / "settings.json",
                {}
            )
            incoming_deleted = self._read_json(
                temp_dir / "deleted.json",
                {}
            )

            local_by_id = {
                item.id: item
                for item in manager.get_all()
            }

            added = 0
            updated = 0
            skipped = 0
            deleted_count = 0

            # Merge vocabulary records by UUID.
            for item in incoming:
                if not item.get("id") or not item.get("word"):
                    skipped += 1
                    continue

                item_id = item["id"]
                incoming_updated = self._timestamp(
                    item.get("updated_at") or item.get("created_at")
                )

                local = local_by_id.get(item_id)

                if local is None:
                    from app.models.vocabulary import Vocabulary
                    new_item = Vocabulary(
                        word=item["word"],
                        data=item.get("data", {}),
                        vocabulary_id=item_id,
                        created_at=item.get("created_at"),
                        updated_at=item.get("updated_at") or item.get("created_at")
                    )
                    manager.add(new_item)
                    local_by_id[item_id] = new_item
                    added += 1
                    self._import_image_for_id(temp_dir, item_id)
                    continue

                local_updated = self._timestamp(
                    getattr(local, "updated_at", None)
                    or getattr(local, "created_at", None)
                )

                if incoming_updated >= local_updated:
                    local.word = item["word"]
                    local.data = item.get("data", {})
                    local.updated_at = (
                        item.get("updated_at")
                        or item.get("created_at")
                        or local.updated_at
                    )
                    updated += 1
                    self._import_image_for_id(temp_dir, item_id)
                else:
                    skipped += 1

            # Merge deletion tombstones.
            deleted_file = self.vocabulary_database_path.parent / "deleted.json"
            local_deleted = self._read_json(deleted_file, {})
            merged_deleted = dict(local_deleted)

            for item_id, deleted_at in incoming_deleted.items():
                incoming_deleted_time = self._timestamp(deleted_at)
                local_deleted_time = self._timestamp(
                    merged_deleted.get(item_id)
                )

                if incoming_deleted_time >= local_deleted_time:
                    merged_deleted[item_id] = deleted_at

                local = local_by_id.get(item_id)
                if local is not None:
                    local_updated = self._timestamp(
                        getattr(local, "updated_at", None)
                        or getattr(local, "created_at", None)
                    )
                    if incoming_deleted_time >= local_updated:
                        manager.delete(local)
                        deleted_count += 1

            # Merge practice IDs as a set/union. Keep visible_fields local.
            local_practice = set(settings.get_practice_ids())
            incoming_practice = set(
                incoming_settings.get("practice_ids", [])
            )
            merged_practice = sorted(local_practice | incoming_practice)

            current_settings = settings.load()
            current_settings["practice_ids"] = merged_practice
            settings.save(current_settings)

            # Save tombstones and vocabulary.
            self._write_json(deleted_file, merged_deleted)
            manager.save()

            # Any new image files not tied to a vocabulary record are harmless
            # but are intentionally not imported.
            return {
                "added": added,
                "updated": updated,
                "skipped": skipped,
                "deleted": deleted_count
            }

    def create_pre_import_backup(self):
        self.backup_directory.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output = self.backup_directory / f"pre_import_{stamp}.zip"
        return self.export_backup(output)

    @staticmethod
    def _read_json(path, default):
        path = Path(path)
        if not path.exists():
            return default

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def _write_json(path, value):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(value, file, ensure_ascii=False, indent=4)

    @staticmethod
    def _timestamp(value):
        if not value:
            return datetime.min

        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(
                tzinfo=None
            )
        except (TypeError, ValueError):
            return datetime.min

    @staticmethod
    def _safe_extract(zip_path, destination):
        destination = Path(destination).resolve()

        with zipfile.ZipFile(zip_path, "r") as archive:
            for member in archive.infolist():
                target = (destination / member.filename).resolve()
                if not str(target).startswith(str(destination)):
                    raise ValueError("Unsafe ZIP entry detected.")

                if member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(member) as source, target.open("wb") as target_file:
                        shutil.copyfileobj(source, target_file)

    def _import_image_for_id(self, extracted_root, vocabulary_id):
        image_root = Path(extracted_root) / "images"
        if not image_root.exists():
            return

        candidates = [
            p for p in image_root.iterdir()
            if p.is_file() and p.stem == vocabulary_id
        ]
        if not candidates:
            return

        self.image_directory.mkdir(parents=True, exist_ok=True)

        # Remove any existing image for this UUID so extensions can change.
        for existing in self.image_directory.iterdir():
            if existing.is_file() and existing.stem == vocabulary_id:
                existing.unlink()

        shutil.copy2(
            candidates[0],
            self.image_directory / candidates[0].name
        )
