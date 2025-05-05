const inputField = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');
const chatContainer = document.getElementById('chat-scroll-container');

function addChatBubble(text, from = 'user') {
  console.log("Adding chat bubble:", text, "from:", from);

  const bubble = document.createElement('div');
  bubble.className = `flex justify-${from === 'user' ? 'end' : 'start'} mt-4`;

  const innerBubble = document.createElement('div');

  // Warna dan alignment yang serasi tapi dibedakan
  const baseClass = "max-w-[70%] p-4 rounded-3xl text-[15px] font-normal shadow-md border";
  const botStyle = "bg-[#F0FDF4] text-[#0F5132] border-emerald-200 rounded-bl-none";
  const userStyle = "bg-[#DBFFEF] text-[#00885C] border-emerald-300/30 rounded-br-none";

  innerBubble.className = `${baseClass} ${from === 'user' ? userStyle : botStyle}`;

  // Isi markdown atau teks polos
  if (from === 'bot') {
    const markdownContainer = document.createElement('div');
    markdownContainer.className = 'prose prose-sm max-w-none';
    try {
      markdownContainer.innerHTML = marked.parse(text);
    } catch (e) {
      console.error("Error parsing markdown:", e);
      markdownContainer.textContent = text;
    }
    innerBubble.appendChild(markdownContainer);
  } else {
    innerBubble.innerHTML = `<p>${text}</p>`;
  }

  bubble.appendChild(innerBubble);
  chatContainer.appendChild(bubble);
  setTimeout(() => {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }, 100);
}


function showLoading() {
  const loadingBubble = document.createElement('div');
  loadingBubble.className = 'flex justify-start mt-2';
  loadingBubble.id = 'loading-bubble';

  const bubbleContent = document.createElement('div');
  bubbleContent.className = 'max-w-[70%] border border-white/20 p-4 rounded-3xl rounded-bl-none text-[16px] font-semibold shadow-md' ;
  
  const dotWrapper = document.createElement('div');
  dotWrapper.className = 'dot-typing';
  dotWrapper.innerHTML = '<span></span><span></span><span></span>';

  bubbleContent.appendChild(dotWrapper);
  loadingBubble.appendChild(bubbleContent);
  chatContainer.appendChild(loadingBubble);
  setTimeout(() => {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }, 100);
}

async function sendMessage() {
  console.log("sendMessage called");
  const userInput = inputField.value.trim();
  if (!userInput) return;

  console.log("User ID:", userId);
  console.log("Current Chat ID:", currentChatId);

  addChatBubble(userInput, 'user');
  inputField.value = '';
  showLoading();

  try {
    if (!currentChatId) {
      const chatTitle = userInput.length > 20 ? userInput.substring(0, 20) + "..." : userInput;
      const createChatRes = await fetch('http://localhost:8000/chat_history/chats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          title: chatTitle
        })
      });
      if (!createChatRes.ok) throw new Error("Failed to create chat");
      const newChat = await createChatRes.json();
      currentChatId = newChat.id;
      fetchChatList();
    }

    console.log("currentChatId before saving user message:", currentChatId);
    const saveUserMsgRes = await fetch('http://localhost:8000/chat_history/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: currentChatId,
        sender: 'user',
        content: userInput
      })
    });
    if (!saveUserMsgRes.ok) throw new Error("Failed to save user message");

    const res = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_input: `Kamu adalah chatbot medis yang hanya dapat memberikan informasi tentang Tuberkulosis (TBC) dan penyakit serupa. Jika pertanyaan tidak terkait dengan TBC atau penyakit terkait, tetapi masih lingkup penyakit, jawab saja. Jika tidak, beri tahu pengguna bahwa kamu hanya dapat memberikan informasi tentang topik tersebut. Pertanyaan: ${userInput}`
      })
    });

    if (!res.ok) {
      throw new Error("Chatbot API response not OK");
    }

    const data = await res.json();
    console.log("Chatbot response data:", data);
    document.getElementById('loading-bubble')?.remove();
    if (data.reply) {
      addChatBubble(data.reply, 'bot');
    } else {
      addChatBubble('⚠️ Respon chatbot kosong.', 'bot');
    }

    const saveBotMsgRes = await fetch('http://localhost:8000/chat_history/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: currentChatId,
        sender: 'bot',
        content: data.reply || ''
      })
    });
    if (!saveBotMsgRes.ok) console.error("Failed to save bot message");

  } catch (err) {
    document.getElementById('loading-bubble')?.remove();
    addChatBubble('⚠️ Gagal menghubungi chatbot.', 'bot');
    console.error(err);
  }
}

sendButton.addEventListener('click', sendMessage);
inputField.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});

function addGreetingMessage() {
  addChatBubble("Hai! Saya Epicare, asisten virtual kamu. Aku di sini buat bantu kamu memahami gejala TBC dan kasih arahan. Gimana kabarmu hari ini?", 'bot');
}

let currentChatId = null;

function getUserIdFromSession() {
  const userStr = sessionStorage.getItem('user');
  if (!userStr) return null;
  try {
    const user = JSON.parse(userStr);
    return user.id || null;
  } catch {
    return null;
  }
}
const userId = getUserIdFromSession();

async function fetchChatList() {
  try {
    console.log("Fetching chat list for userId:", userId);
    if (!userId) {
      console.error("User ID not found in sessionStorage.");
      document.getElementById('chat-history').innerHTML = '<p class="p-4">User not logged in. Please login again.</p>';
      return;
    }
    const res = await fetch(`http://localhost:8000/chat_history/chats/${userId}`);
    if (!res.ok) {
      console.error("Failed to fetch chat list, status:", res.status);
      throw new Error("Failed to fetch chat list");
    }
    const chats = await res.json();
    console.log("Chat list fetched:", chats);
    renderChatList(chats);
  } catch (error) {
    console.error(error);
    renderChatList([]);
  }
}

function renderChatList(chats) {
  const container = document.getElementById('chat-history');
  container.innerHTML = '';
  chats.forEach(chat => {
    const item = document.createElement('div');
    item.className = `p-3 bg-white/10 hover:bg-white/20 rounded-md cursor-pointer transition flex justify-between items-center ${
      chat.id === currentChatId ? 'border border-emerald-400' : ''
    }`;

    const titleContainer = document.createElement('div');
    titleContainer.className = 'flex items-center flex-grow cursor-pointer space-x-2';

    const titleText = document.createElement('div');
    titleText.className = 'text-gray-800 font-semibold mb-1';
    titleText.style.flex = '1 1 auto';
    titleText.style.fontSize = '14px';
    const maxTitleLength = 10;
    if (chat.title.length > maxTitleLength) {
      titleText.textContent = chat.title.substring(0, maxTitleLength) + '...';
    } else {
      titleText.textContent = chat.title;
    }

    const titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.value = chat.title;
    titleInput.className = 'hidden rounded px-2 py-1 text-black text-sm font-semibold w-full';

    titleContainer.appendChild(titleText);
    titleContainer.appendChild(titleInput);

    const createdAt = document.createElement('div');
    createdAt.className = 'text-sm 60';
    createdAt.textContent = new Date(chat.created_at).toLocaleDateString();

    const editButton = document.createElement('button');
    editButton.className = 'text-yellow-400 hover:text-yellow-600 ml-4';
    editButton.title = 'Edit judul percakapan';
    editButton.innerHTML = '<i class="fa-solid fa-pen-to-square"></i>';

    const deleteButton = document.createElement('button');
    deleteButton.className = 'text-red-500 hover:text-red-700 ml-4';
    deleteButton.title = 'Hapus percakapan';
    deleteButton.innerHTML = '<i class="fa-solid fa-trash"></i>';

    item.appendChild(titleContainer);
    item.appendChild(createdAt);
    item.appendChild(editButton);
    item.appendChild(deleteButton);

    editButton.addEventListener('click', (e) => {
      e.stopPropagation();
      titleText.classList.add('hidden');
      titleInput.classList.remove('hidden');
      titleInput.focus();
    });

    async function saveTitleUpdate() {
      const newTitle = titleInput.value.trim();
      if (newTitle === '') {
        alert('Judul tidak boleh kosong.');
        titleInput.value = chat.title;
        titleInput.classList.add('hidden');
        titleText.classList.remove('hidden');
        return;
      }
      if (newTitle === chat.title) {
        titleInput.classList.add('hidden');
        titleText.classList.remove('hidden');
        return;
      }
      try {
        const res = await fetch(`http://localhost:8000/chat_history/chats/${chat.id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: newTitle })
        });
        if (!res.ok) throw new Error('Gagal memperbarui judul');
        const updatedChat = await res.json();
        chat.title = updatedChat.title;
        if (updatedChat.title.length > maxTitleLength) {
          titleText.textContent = updatedChat.title.substring(0, maxTitleLength) + '...';
        } else {
          titleText.textContent = updatedChat.title;
        }
      } catch (error) {
        alert('Gagal memperbarui judul. Silakan coba lagi.');
        console.error(error);
        titleInput.value = chat.title;
      } finally {
        titleInput.classList.add('hidden');
        titleText.classList.remove('hidden');
      }
    }

    titleInput.addEventListener('blur', saveTitleUpdate);
    titleInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        titleInput.blur();
      }
    });

    deleteButton.addEventListener('click', async (e) => {
      e.stopPropagation();
      if (!confirm('Apakah Anda yakin ingin menghapus percakapan ini?')) return;
      try {
        const res = await fetch(`http://localhost:8000/chat_history/chats/${chat.id}`, {
          method: 'DELETE',
        });
        if (!res.ok) throw new Error('Gagal menghapus percakapan');
        if (chat.id === currentChatId) {
          currentChatId = null;
          chatContainer.innerHTML = '';
        }
        fetchChatList();
      } catch (error) {
        alert('Gagal menghapus percakapan. Silakan coba lagi.');
        console.error(error);
      }
    });

    item.onclick = () => loadChat(chat.id);

    container.appendChild(item);
  });
}

async function loadChat(chatId) {
  currentChatId = chatId;

  chatContainer.innerHTML = '';

  try {
    const res = await fetch(`http://localhost:8000/chat_history/messages/${chatId}`);
    if (!res.ok) throw new Error("Failed to fetch messages");
    const messages = await res.json();
    messages.forEach(msg => addChatBubble(msg.content, msg.sender));
  } catch (error) {
    console.error(error);
    addChatBubble("⚠️ Gagal memuat pesan chat.", "bot");
  }

  fetchChatList();
}

document.getElementById('new-chat-btn').addEventListener('click', () => {
  currentChatId = null;
  chatContainer.innerHTML = '';
  fetchChatList();
});

fetchChatList();
addGreetingMessage();
