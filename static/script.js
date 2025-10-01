// 🎵 Drag & Drop para reordenar canciones
document.addEventListener("DOMContentLoaded", () => {
  const list = document.querySelector("ul");
  let draggedItem = null;

  if (list) {
    list.querySelectorAll("li").forEach(item => {
      item.setAttribute("draggable", true);

      item.addEventListener("dragstart", (e) => {
        draggedItem = item;
        setTimeout(() => item.classList.add("dragging"), 0);
      });

      item.addEventListener("dragend", (e) => {
        item.classList.remove("dragging");
        draggedItem = null;
      });
    });

    list.addEventListener("dragover", (e) => {
      e.preventDefault();
      const afterElement = getDragAfterElement(list, e.clientY);
      if (afterElement == null) {
        list.appendChild(draggedItem);
      } else {
        list.insertBefore(draggedItem, afterElement);
      }
    });

    function getDragAfterElement(container, y) {
      const draggableElements = [...container.querySelectorAll("li:not(.dragging)")];

      return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
          return { offset: offset, element: child };
        } else {
          return closest;
        }
      }, { offset: Number.NEGATIVE_INFINITY }).element;
    }
  }
});
