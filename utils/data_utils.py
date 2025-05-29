import csv

import csv
from models.projects import Project  # Updated to match the new Project class


def is_duplicate_project(project_name: str, seen_names: set) -> bool:
    """Checks if a project name has already been encountered."""
    return project_name in seen_names


def is_complete_project(project: dict, required_keys: list) -> bool:
    """Ensures all required attributes exist in a project dictionary."""
    return all(key in project for key in required_keys)


def save_projects_to_csv(projects: list, filename: str):
    """Saves project data into a CSV file."""
    if not projects:
        print("No projects to save.")
        return

    # Use field names from the Project model
    fieldnames = Project.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(projects)
    
    print(f"Saved {len(projects)} projects to '{filename}'.")
