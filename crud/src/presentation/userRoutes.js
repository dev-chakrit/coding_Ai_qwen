const express = require('express');
const router = express.Router();
const userService = require('../application/service/userService');

// GET /api/users
router.get('/users', async (req, res) => {
  try {
    const users = await userService.getAllUsers();
    res.status(200).json(users);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// GET /api/users/:id
router.get('/users/:id', async (req, res) => {
  try {
    const userId = req.params.id;
    const user = await userService.getUserById(userId);
    res.status(200).json(user);
  } catch (error) {
    res.status(404).json({ message: error.message });
  }
});

// POST /api/users
router.post('/users', async (req, res) => {
  const userData = req.body;
  try {
    const user = await userService.createUser(userData);
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// PUT /api/users/:id
router.put('/users/:id', async (req, res) => {
  const userId = req.params.id;
  const updateData = req.body;
  try {
    const user = await userService.updateUser(userId, updateData);
    res.status(200).json(user);
  } catch (error) {
    res.status(404).json({ message: error.message });
  }
});

// DELETE /api/users/:id
router.delete('/users/:id', async (req, res) => {
  const userId = req.params.id;
  try {
    await userService.deleteUser(userId);
    res.status(200).json({ message: `User ${userId} deleted successfully` });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;