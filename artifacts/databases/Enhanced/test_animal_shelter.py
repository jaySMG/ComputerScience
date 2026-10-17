"""
Tests for the AnimalShelter database access module.

MongoDB interactions are mocked so these tests do not change
the actual animal shelter database.
"""

from unittest.mock import MagicMock, patch

import pytest

from animal_shelter import AnimalShelter


@pytest.fixture
def shelter():
    """Create an AnimalShelter object with a mocked MongoDB connection."""

    with patch("animal_shelter.MongoClient") as mock_client:
        mock_collection = MagicMock()

        mock_database = MagicMock()
        mock_database.__getitem__.return_value = mock_collection

        mock_client.return_value.__getitem__.return_value = mock_database

        animal_shelter = AnimalShelter()
        animal_shelter.collection = mock_collection

        return animal_shelter


def test_create_inserts_record(shelter):
    """Verify that create sends an animal record to MongoDB."""

    animal = {
        "animal_id": "TEST001",
        "animal_type": "Dog",
        "name": "Test Dog"
    }

    result = shelter.create(animal)

    shelter.collection.insert_one.assert_called_once_with(animal)
    assert result is True


def test_create_rejects_empty_data(shelter):
    """Verify that create rejects an empty animal record."""

    with pytest.raises(ValueError):
        shelter.create({})


def test_read_uses_query(shelter):
    """Verify that read sends the correct query to MongoDB."""

    query = {"animal_type": "Dog"}

    expected_records = [
        {"animal_id": "A1", "animal_type": "Dog"},
        {"animal_id": "A2", "animal_type": "Dog"}
    ]

    shelter.collection.find.return_value = expected_records

    result = shelter.read(query)

    shelter.collection.find.assert_called_once_with(query)
    assert result == expected_records


def test_read_rejects_invalid_query(shelter):
    """Verify that read requires a dictionary query."""

    with pytest.raises(ValueError):
        shelter.read("animal_type=Dog")


def test_update_one_record(shelter):
    """Verify that update can modify one matching record."""

    shelter.collection.update_one.return_value.modified_count = 1

    query = {"animal_id": "TEST001"}
    update_data = {"$set": {"name": "Updated Dog"}}

    result = shelter.update(query, update_data)

    shelter.collection.update_one.assert_called_once_with(
        query,
        update_data
    )

    assert result == 1


def test_update_many_records(shelter):
    """Verify that update can modify multiple matching records."""

    shelter.collection.update_many.return_value.modified_count = 3

    query = {"animal_type": "Dog"}
    update_data = {"$set": {"test_status": True}}

    result = shelter.update(
        query,
        update_data,
        update_many=True
    )

    shelter.collection.update_many.assert_called_once_with(
        query,
        update_data
    )

    assert result == 3


def test_delete_one_record(shelter):
    """Verify that delete can remove one matching record."""

    shelter.collection.delete_one.return_value.deleted_count = 1

    query = {"animal_id": "TEST001"}

    result = shelter.delete(query)

    shelter.collection.delete_one.assert_called_once_with(query)
    assert result == 1


def test_delete_many_records(shelter):
    """Verify that delete can remove multiple matching records."""

    shelter.collection.delete_many.return_value.deleted_count = 4

    query = {"animal_type": "Dog"}

    result = shelter.delete(query, delete_many=True)

    shelter.collection.delete_many.assert_called_once_with(query)
    assert result == 4

def test_aggregate_runs_pipeline(shelter):
    """Verify that aggregate sends the pipeline to MongoDB."""

    pipeline = [
        {
            "$group": {
                "_id": "$breed",
                "count": {"$sum": 1}
            }
        }
    ]

    expected_results = [
        {"_id": "Labrador Retriever Mix", "count": 5},
        {"_id": "German Shepherd", "count": 3}
    ]

    shelter.collection.aggregate.return_value = expected_results

    result = shelter.aggregate(pipeline)

    shelter.collection.aggregate.assert_called_once_with(pipeline)
    assert result == expected_results


def test_aggregate_rejects_invalid_pipeline(shelter):
    """Verify that aggregate requires a non-empty list."""

    with pytest.raises(ValueError):
        shelter.aggregate({})


def test_get_breed_counts_uses_aggregation(shelter):
    """Verify that breed counts use a MongoDB aggregation pipeline."""

    expected_results = [
        {"_id": "Labrador Retriever Mix", "count": 5},
        {"_id": "German Shepherd", "count": 3}
    ]

    shelter.collection.aggregate.return_value = expected_results

    result = shelter.get_breed_counts()

    shelter.collection.aggregate.assert_called_once()

    assert result == [
        {
            "breed": "Labrador Retriever Mix",
            "count": 5
        },
        {
            "breed": "German Shepherd",
            "count": 3
        }
    ]


def test_get_breed_counts_accepts_query(shelter):
    """Verify that breed counts can be limited by a MongoDB query."""

    shelter.collection.aggregate.return_value = [
        {
            "_id": "Labrador Retriever Mix",
            "count": 4
        }
    ]

    query = {"animal_type": "Dog"}

    result = shelter.get_breed_counts(query)

    pipeline = shelter.collection.aggregate.call_args.args[0]

    assert pipeline[0] == {"$match": query}
    assert result == [
        {
            "breed": "Labrador Retriever Mix",
            "count": 4
        }
    ]


def test_create_indexes(shelter):
    """Verify that indexes are created for commonly queried fields."""

    shelter.collection.create_index.side_effect = [
        "animal_type_1",
        "breed_1",
        "sex_upon_outcome_1",
        "age_upon_outcome_in_weeks_1"
    ]

    result = shelter.create_indexes()

    assert shelter.collection.create_index.call_count == 4

    assert result == [
        "animal_type_1",
        "breed_1",
        "sex_upon_outcome_1",
        "age_upon_outcome_in_weeks_1"
    ]

def test_get_indexes_returns_database_indexes(shelter):
    """Verify that existing MongoDB indexes can be retrieved."""

    expected_indexes = {
        "_id_": {
            "key": [("_id", 1)],
            "v": 2
        },
        "breed_1": {
            "key": [("breed", 1)],
            "v": 2
        }
    }

    shelter.collection.index_information.return_value = expected_indexes

    result = shelter.get_indexes()

    shelter.collection.index_information.assert_called_once_with()
    assert result == expected_indexes