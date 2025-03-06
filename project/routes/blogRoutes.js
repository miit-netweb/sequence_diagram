const express = require('express');
const router = express.Router();
const { getAllBlogs, createBlog, updateBlog, deleteBlog } = require('../controllers/blogController');
const authenticateToken = require('../middleware/auth');

router.get('/', getAllBlogs);
router.post('/', authenticateToken, createBlog);
router.put('/:id', authenticateToken, updateBlog);
router.delete('/:id', authenticateToken, deleteBlog);

module.exports = router;