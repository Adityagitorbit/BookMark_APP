document.addEventListener('DOMContentLoaded', () => {
    // Fetch Categories
    async function loadCategories() {
        const response = await fetch('/api/categories');
        const categories = await response.json();
        const categoriesList = document.getElementById('categories-list');
        categoriesList.innerHTML = '';
        categories.forEach(category => {
            categoriesList.innerHTML += `<li>${category.name}</li>`;
        });
    }

    // Fetch Bookmarks
    async function loadBookmarks() {
        const response = await fetch('/api/bookmarks');
        const bookmarks = await response.json();
        const bookmarksList = document.getElementById('bookmarks-list');
        bookmarksList.innerHTML = '';
        bookmarks.forEach(bookmark => {
            bookmarksList.innerHTML += `<li><a href="${bookmark.url}" target="_blank">${bookmark.title}</a></li>`;
        });
    }

    // Add Bookmark
    document.getElementById('add-bookmark-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('bookmark-title').value;
        const url = document.getElementById('bookmark-url').value;
        const description = document.getElementById('bookmark-description').value;

        await fetch('/api/bookmarks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, url, description })
        });

        loadBookmarks();
    });

    loadCategories();
    loadBookmarks();
});
