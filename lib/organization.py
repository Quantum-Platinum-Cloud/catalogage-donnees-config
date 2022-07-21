import json
from pathlib import Path
from typing import List

from frictionless import Resource, validate
from frictionless.report import Report

from .entities import Organization


def get_organizations_path(path: Path) -> List[Path]:
    org_paths: List[Path] = []
    for orgdir in Path(path).iterdir():
        org_path = orgdir / "organization.json"
        org_paths.append(org_path)

    return org_paths


def get_organizations(path: Path) -> List[Organization]:
    organizations: List[Organization] = []

    for org_path in get_organizations_path(path):
        data = json.loads(org_path.read_text())
        organization = data[0]
        new_organization = Organization(
            siret=organization["siret"], name=organization["name"]
        )
        organizations.append(new_organization)

    return organizations


def contains_one_organization_per_file(path: Path) -> bool:
    data = json.loads(path.read_text())
    return len(data) == 1


def get_organization_validation_report(path: Path) -> Report:

    template = {
        "path": "...",
        "name": "organization",
        "profile": "tabular-data-resource",
        "scheme": "file",
        "format": "json",
        "hashing": "md5",
        "encoding": "utf-8",
        "schema": {
            "fields": [
                {
                    "name": "name",
                    "title": "Nom de l'organisation",
                    "type": "string",
                },
                {
                    "name": "siret",
                    "title": "Numéro SIRET de l'organisation",
                    "type": "string",
                },
            ]
        },
    }
    descriptor = template.copy()
    descriptor["path"] = str(path)

    with Resource(descriptor=descriptor) as resource:
        report = validate(resource, type="resource")
    return report