## Notes API

This project implements a simple Notes API with full CRUD functionality.

### What’s Included

The API provides the following endpoints:

- POST /notes – Create a new note

- GET /notes – Retrieve all notes

- GET /notes/{id} – Retrieve a specific note by ID

- PUT /notes/{id} – Update an existing note

- DELETE /notes/{id} – Delete a note

Each endpoint returns appropriate HTTP status codes depending on the result (e.g., success, not found, or invalid input).

Data Validation

Pydantic schemas are used to handle validation and data structure for requests and responses:

- NoteCreate – used when creating a note

- NoteUpdate – used when updating a note

- NoteResponse - used to specify response content