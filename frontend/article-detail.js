const urlParams = new URLSearchParams(window.location.search);
const articleId = urlParams.get("id");

async function fetchArticleDetail() {
  try {
    const res = await fetch(`/api/articles/${articleId}`);
    const article = await res.json();

    document.getElementById("article-title").textContent = article.title;
    document.getElementById("article-author").textContent = `Penulis: ${
      article.author
    } | Dipublikasikan: ${new Date(article.published_at).toLocaleDateString(
      "id-ID"
    )}`;
    document.getElementById("article-image").src = article.url_to_image;
    document.getElementById("article-description").textContent =
      article.description;
    document.getElementById("article-content").innerHTML = article.content;
    document.getElementById("article-url").href = article.url;
  } catch (error) {
    console.error("Gagal memuat detail artikel:", error);
    document.getElementById("article-content").textContent =
      "Maaf, terjadi kesalahan saat memuat artikel.";   
  }
}

fetchArticleDetail();
