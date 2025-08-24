import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/contacts/";

function App() {
  const [contacts, setContacts] = useState([]);
  const [form, setForm] = useState({ id: null, name: "", email: "", phone: "" });
  const [editing, setEditing] = useState(false);

  // Fetch contacts
  const fetchContacts = async () => {
    try {
      const res = await axios.get(API_URL);
      setContacts(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  // Input handler
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Add contact
  const addContact = async () => {
    try {
      await axios.post(API_URL, form);
      setForm({ id: null, name: "", email: "", phone: "" });
      fetchContacts();
    } catch (err) {
      console.error(err);
    }
  };

  // Update contact
  const updateContact = async () => {
    try {
      await axios.put(`${API_URL}${form.id}`, form);
      setEditing(false);
      setForm({ id: null, name: "", email: "", phone: "" });
      fetchContacts();
    } catch (err) {
      console.error(err);
    }
  };

  // Delete contact
  const deleteContact = async (id) => {
    try {
      await axios.delete(`${API_URL}${id}`);
      fetchContacts();
    } catch (err) {
      console.error(err);
    }
  };

  // Edit mode
  const editContact = (contact) => {
    setForm(contact);
    setEditing(true);
  };

  useEffect(() => {
    fetchContacts();
  }, []);

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">📒 Contact Manager</h1>

      {/* Contact Form */}
      <div className="card mb-4">
        <div className="card-header">
          {editing ? "Edit Contact" : "Add New Contact"}
        </div>
        <div className="card-body">
          <div className="row g-2">
            <div className="col-md-3">
              <input
                type="text"
                name="name"
                placeholder="Name"
                value={form.name}
                onChange={handleChange}
                className="form-control"
              />
            </div>
            <div className="col-md-3">
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={form.email}
                onChange={handleChange}
                className="form-control"
              />
            </div>
            <div className="col-md-3">
              <input
                type="text"
                name="phone"
                placeholder="Phone"
                value={form.phone}
                onChange={handleChange}
                className="form-control"
              />
            </div>
            <div className="col-md-3">
              {editing ? (
                <button
                  onClick={updateContact}
                  className="btn btn-primary w-100"
                >
                  Update
                </button>
              ) : (
                <button
                  onClick={addContact}
                  className="btn btn-success w-100"
                >
                  Add
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Contact List */}
      <div className="card">
        <div className="card-header">All Contacts</div>
        <div className="card-body">
          <table className="table table-bordered table-striped">
            <thead className="table-dark">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {contacts.map((c) => (
                <tr key={c.id}>
                  <td>{c.id}</td>
                  <td>{c.name}</td>
                  <td>{c.email}</td>
                  <td>{c.phone}</td>
                  <td>
                    <button
                      className="btn btn-warning btn-sm me-2"
                      onClick={() => editContact(c)}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => deleteContact(c.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
              {contacts.length === 0 && (
                <tr>
                  <td colSpan="5" className="text-center text-muted">
                    No contacts found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;
