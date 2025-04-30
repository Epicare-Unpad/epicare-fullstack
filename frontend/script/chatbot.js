const inputField = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');
const chatContainer = document.getElementById('chat-scroll-container');

function addChatBubble(text, from = 'user') {
  console.log("Adding chat bubble:", text, "from:", from);
  const bubble = document.createElement('div');
  bubble.className = `flex justify-${from === 'user' ? 'end' : 'start'} mt-4`;

  const innerBubble = document.createElement('div');
  innerBubble.className = `max-w-[70%] ${
    from === 'user'
      ? 'bg-[#DBFFEF] text-[#00885C] border border-emerald-300/30 rounded-br-none'
      : 'bg-[#01BF81] border border-white/20 text-white rounded-bl-none'
  } p-4 rounded-3xl text-[16px] font-semibold shadow-md`;

  if (from === 'bot') {
    const markdownContainer = document.createElement('div');
    markdownContainer.className = 'prose prose-sm prose-invert max-w-none';
    markdownContainer.innerHTML = marked.parse(text);
    innerBubble.appendChild(markdownContainer);
  } else {
    innerBubble.innerHTML = `<p>${text}</p>`;
  }

  bubble.appendChild(innerBubble);
  if (!chatContainer) {
    console.error("chatContainer is null or undefined");
  } else {
    chatContainer.appendChild(bubble);
    setTimeout(() => {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 100);
  }
}

function showLoading() {
  const loadingBubble = document.createElement('div');
  loadingBubble.className = 'flex justify-start mt-4';
  loadingBubble.id = 'loading-bubble';

  const bubbleContent = document.createElement('div');
  bubbleContent.className = 'max-w-[70%] bg-[#01BF81] border border-white/20 p-4 rounded-3xl rounded-bl-none text-[16px] font-semibold shadow-md text-white';
  
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
    // If no current chat, create a new chat first
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
      fetchChatList(); // Refresh chat list sidebar
    }

    // Send user message to backend to save
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

    // Send user input to chatbot API
    const res = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_input: `Kamu adalah chatbot medis yang hanya dapat memberikan informasi tentang Tuberkulosis (TBC) dan penyakit serupa. Jika pertanyaan tidak terkait dengan TBC atau penyakit terkait, tetapi masih lingkup penyakit, jawab saja. Jika tidak, beri tahu pengguna bahwa kamu hanya dapat memberikan informasi tentang topik tersebut. Pertanyaan: ${userInput}`
      })
    });

    const data = await res.json();
    document.getElementById('loading-bubble')?.remove();
    addChatBubble(data.reply, 'bot');

    // Save chatbot response message
    const saveBotMsgRes = await fetch('http://localhost:8000/chat_history/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: currentChatId,
        sender: 'bot',
        content: data.reply
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

// Fetch actual user ID from session or authentication context
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
      document.getElementById('chat-history').innerHTML = '<p class="text-white p-4">User not logged in. Please login again.</p>';
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

    // Create title container with editable functionality
    const titleContainer = document.createElement('div');
    titleContainer.className = 'flex items-center flex-grow cursor-pointer space-x-2';

    const titleText = document.createElement('div');
    titleText.className = 'text-white font-semibold mb-1';
    titleText.style.flex = '1 1 auto';
    titleText.style.fontSize = '14px'; // reduce font size by 1-2px
    // Truncate title if longer than 10 characters
    const maxTitleLength = 10;
    if (chat.title.length > maxTitleLength) {
      titleText.textContent = chat.title.substring(0, maxTitleLength) + '...';
    } else {
      titleText.textContent = chat.title;
    }

    // Create input for editing title, hidden by default
    const titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.value = chat.title;
    titleInput.className = 'hidden rounded px-2 py-1 text-black text-sm font-semibold w-full';

    titleContainer.appendChild(titleText);
    titleContainer.appendChild(titleInput);

    // Created at element
    const createdAt = document.createElement('div');
    createdAt.className = 'text-sm text-white/60';
    createdAt.textContent = new Date(chat.created_at).toLocaleDateString();

    // Edit button/icon
    const editButton = document.createElement('button');
    editButton.className = 'text-yellow-400 hover:text-yellow-600 ml-4';
    editButton.title = 'Edit judul percakapan';
    editButton.innerHTML = '<i class="fa-solid fa-pen-to-square"></i>';

    // Delete button
    const deleteButton = document.createElement('button');
    deleteButton.className = 'text-red-500 hover:text-red-700 ml-4';
    deleteButton.title = 'Hapus percakapan';
    deleteButton.innerHTML = '<i class="fa-solid fa-trash"></i>';

    // Append elements to item
    item.appendChild(titleContainer);
    item.appendChild(createdAt);
    item.appendChild(editButton);
    item.appendChild(deleteButton);

    // Event: click edit button to toggle input visibility
    editButton.addEventListener('click', (e) => {
      e.stopPropagation();
      titleText.classList.add('hidden');
      titleInput.classList.remove('hidden');
      titleInput.focus();
    });

    // Function to save title update
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
        // No change
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
        // Truncate updated title if longer than 10 characters
        const maxTitleLength = 10;
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

    // Event: blur on input to save
    titleInput.addEventListener('blur', saveTitleUpdate);

    // Event: enter key on input to save
    titleInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        titleInput.blur();
      }
    });

    // Delete button event
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

    // Clicking on item loads chat
    item.onclick = () => loadChat(chat.id);

    container.appendChild(item);
  });
}

async function loadChat(chatId) {
  currentChatId = chatId;

  
  // Clear current chat
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

  fetchChatList(); // Re-render sidebar to highlight current
}

// Handle "New Chat"
document.getElementById('new-chat-btn').addEventListener('click', () => {
  currentChatId = null; // Reset current chat ID
  chatContainer.innerHTML = ''; // Clear chat area
  fetchChatList(); // Refresh chat list sidebar
});

// Load on first run
fetchChatList();
addGreetingMessage();
