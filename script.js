function openMessageFrom(title, media, caption) {
  document.getElementById("message_title").value = title;
  document.getElementById("message_image").value = media;
  document.getElementById("message_caption").value = caption;
  document.getElementById("message_popup").classList.add("active");
}

function closeMessageForm() {
  document.getElementById("message_popup").classList.remove("active");
}
