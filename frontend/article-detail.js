document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const articleId = urlParams.get("id");

  const titleEl = document.getElementById("article-title");
  const dateEl = document.getElementById("publish-date");
  const authorEl = document.getElementById("article-author");
  const imageEl = document.getElementById("article-image");
  const contentEl = document.getElementById("article-content");
  const urlContainer = document.getElementById("article-source");
  const urlLink = document.getElementById("article-url");
  const urlText = document.getElementById("article-url-text");

  if (!articleId) {
    titleEl.textContent = "Artikel tidak ditemukan";
    return;
  }

  fetch(`http://127.0.0.1:8000/api/articles/${articleId}`)
    .then(response => {
      if (!response.ok) throw new Error("Artikel tidak ditemukan");
      return response.json();
    })
    .then(article => {
      titleEl.textContent = article.title || "Tanpa Judul";
      dateEl.textContent = article.published_at
        ? new Date(article.published_at).toLocaleDateString("id-ID")
        : "Tanggal tidak tersedia";
      authorEl.textContent = article.author || "Penulis Tidak Diketahui";

      if (article.url_to_image) {
        imageEl.src = article.url_to_image;
        imageEl.classList.remove("hidden");
      } else {
        imageEl.classList.add("hidden");
      }

      contentEl.innerHTML = article.content ? marked.parse(article.content) : "Konten tidak tersedia";

      if (article.url) {
        urlLink.href = article.url;
        urlText.textContent = article.url;
        urlContainer.classList.remove("hidden");
      } else {
        urlText.textContent = "Tidak tersedia";
        urlContainer.classList.add("hidden");
      }
    })
    .catch(error => {
      console.error(error);
      titleEl.textContent = error.message || "Gagal memuat artikel.";
    });
});
