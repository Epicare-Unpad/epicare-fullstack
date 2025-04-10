const articles = [
  {
    title: "Mengenal TBC dan Cara Pencegahannya",
    description: "Tuberkulosis masih menjadi ancaman serius di negara tropis. Pelajari gejala dan cara penanganannya.",
    link: "https://www.alodokter.com/tuberkulosis"
  },
  {
    title: "Waspadai Malaria Saat Musim Hujan",
    description: "Nyamuk Anopheles menjadi penyebab utama malaria. Kenali cara menghindarinya.",
    link: "https://www.halodoc.com/artikel/ini-penyebab-malaria-yang-perlu-diwaspadai"
  },
  {
    title: "Apa Itu Hepatitis dan Jenis-Jenisnya",
    description: "Hepatitis adalah peradangan hati yang bisa disebabkan virus.",
    link: "https://primayahospital.com/penyakit-dalam/jenis-hepatitis/"
  },
  {
    title: "Kenali Gejala Demam Berdarah",
    description: "Demam berdarah disebabkan oleh virus dengue melalui gigitan nyamuk Aedes aegypti.",
    link: "https://www.alodokter.com/demam-berdarah"
  },
  {
    title: "Tips Menjaga Imunitas Tubuh",
    description: "Imun tubuh penting untuk melawan infeksi. Simak cara meningkatkan daya tahan tubuh.",
    link: "https://www.alodokter.com/berbagai-cara-meningkatkan-imunitas-tubuh-agar-tidak-mudah-sakit"
  },
  {
    title: "Fakta Tentang Penyakit Chikungunya",
    description: "Chikungunya disebabkan oleh virus yang dibawa nyamuk, dengan gejala mirip DBD.",
    link: "https://www.alodokter.com/chikungunya"
  },
  {
    title: "Cara Efektif Mencegah Cacingan",
    description: "Cacingan sering menyerang anak-anak. Ini cara mencegah dan mengobatinya.",
    link: "https://halosehat.com/penyakit/cacingan/cara-mencegah-cacingan"
  },
  {
    title: "Gejala dan Pencegahan Leptospirosis",
    description: "Penyakit ini berasal dari air kencing hewan yang terinfeksi, biasanya saat banjir.",
    link: "https://www.alodokter.com/leptospirosis"
  },
  {
    title: "Mengenal Penyakit Diare dan Penanganannya",
    description: "Diare bisa disebabkan oleh infeksi bakteri atau virus. Ini cara mengatasinya.",
    link: "https://www.alodokter.com/diare"
  }
];

const listContainer = document.getElementById("article-list");
const searchInput = document.getElementById("search");
const themeBtn = document.getElementById("toggle-theme");

function renderArticles(filteredArticles) {
  listContainer.innerHTML = "";
  filteredArticles.forEach(article => {
    listContainer.innerHTML += `
      <div class="bg-white rounded-2xl shadow-md p-5 hover:shadow-lg transition duration-300">
        <h2 class="text-xl font-semibold mb-2 text-green-800">${article.title}</h2>
        <p class="text-sm text-gray-700 mb-4">${article.description}</p>
        <a href="${article.link}" target="_blank" rel="noopener noreferrer" class="inline-block bg-green-600 text-white px-4 py-2 rounded-xl hover:bg-green-700 text-sm">Baca Selengkapnya</a>
      </div>
    `;
  });
}

renderArticles(articles);

searchInput.addEventListener("input", () => {
  const keyword = searchInput.value.toLowerCase();
  const filtered = articles.filter(article =>
    article.title.toLowerCase().includes(keyword) ||
    article.description.toLowerCase().includes(keyword)
  );
  renderArticles(filtered);
});

themeBtn.addEventListener("click", () => {
  document.body.classList.toggle("bg-green-50");
  document.body.classList.toggle("bg-gray-900");
  document.body.classList.toggle("text-white");
});
