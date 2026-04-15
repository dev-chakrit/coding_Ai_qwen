module.exports = {
  create: (data) => ({ id: Date.now().toString(), ...data }),
  findById: (id) => {
    // Mock implementation for now
    return { id: id, name: "Test User", email: "test@example.com" };
  },
  findAll: () => [
    { id: "1", name: "Alice", email: "alice@example.com" },
    { id: "2", name: "Bob", email: "bob@example.com" }
  ],
  update: (id, data) => ({ id: id, ...data }),
  delete: (id) => ({ id: id, success: true })
};