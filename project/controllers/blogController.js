const Blog = require('../models/Blog');

const getAllBlogs = async (req, res) => {
  try {
    const blogs = await Blog.find().populate('author', 'username');
    res.json(blogs);
  } catch (err) {
    res.status(500).send(err.message);
  }
};

const createBlog = async (req, res) => {
  try {
    const blog = new Blog({
      title: req.body.title,
      content: req.body.content,
      author: req.user.userId,
    });
    await blog.save();
    res.status(201).send('Blog created');
  } catch (err) {
    res.status(500).send(err.message);
  }
};

const updateBlog = async (req, res) => {
  try {
    const blog = await Blog.findById(req.params.id);
    if (!blog) return res.status(404).send('Blog not found');
    if (blog.author.toString() !== req.user.userId) return res.sendStatus(403);

    blog.title = req.body.title;
    blog.content = req.body.content;
    await blog.save();
    res.send('Blog updated');
  } catch (err) {
    res.status(500).send(err.message);
  }
};

const deleteBlog = async (req, res) => {
  try {
    const blog = await Blog.findById(req.params.id);
    if (!blog) return res.status(404).send('Blog not found');
    if (blog.author.toString() !== req.user.userId) return res.sendStatus(403);

    await Blog.findByIdAndDelete(req.params.id);
    res.send('Blog deleted');
  } catch (err) {
    res.status(500).send(err.message);
  }
};

module.exports = { getAllBlogs, createBlog, updateBlog, deleteBlog };