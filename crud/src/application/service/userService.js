const userRepository = require('../infrastructure/repository/userRepository');

// Domain service layer
class UserService {
  constructor() {
    this.userRepository = userRepository;
  }

  async createUser(userData) {
    // Validation logic can go here
    const user = this.userRepository.create(userData);
    return user;
  }

  async getUserById(userId) {
    const user = this.userRepository.findById(userId);
    if (!user) {
      throw new Error("User not found");
    }
    return user;
  }

  async getAllUsers() {
    return this.userRepository.findAll();
  }

  async updateUser(userId, updateData) {
    // Check if user exists first
    await this.getUserById(userId);
    const user = this.userRepository.update(userId, updateData);
    return user;
  }

  async deleteUser(userId) {
    return this.userRepository.delete(userId);
  }
}

module.exports = new UserService();