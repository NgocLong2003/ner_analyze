document.addEventListener("DOMContentLoaded", function () {
    const textElements = document.querySelectorAll(".entity-text");

    textElements.forEach(textElement => {
        textElement.addEventListener("mouseover", function () {
            // Tạo tooltip container
            const tooltip = document.createElement("div");
            tooltip.classList.add("tooltip");

            // Lấy nội dung meaning từ data-attribute
            const meaning = textElement.getAttribute("data-meaning");

            // Tạo phần hiển thị nội dung meaning
            const meaningDiv = document.createElement("div");
            meaningDiv.innerText = meaning;
            tooltip.appendChild(meaningDiv);

            // Nếu meaning rỗng (được chuyển thành "Chưa có chú giải cho từ này"), thêm nút tra cứu
            if (meaning === "Chưa có chú giải cho từ này") {
                const wikiButton = document.createElement("button");
                wikiButton.innerText = "Tra cứu Wikipedia";
                wikiButton.addEventListener("click", function (e) {
                    e.stopPropagation(); // Ngăn tooltip bị xóa khi click vào nút
                    // Lấy nội dung từ (entity text) để gửi truy vấn
                    const query = textElement.innerText.trim();
                    // Chuyển hướng đến backend /search với query (có thể thêm query string nếu cần)
                    window.location.href = `/search?query=${encodeURIComponent(query)}`;
                });
                // Thêm nút vào tooltip (có thể thêm break line nếu cần)
                tooltip.appendChild(document.createElement("br"));
                tooltip.appendChild(wikiButton);
            }

            // Thêm tooltip vào body
            document.body.appendChild(tooltip);

            // Tính toán vị trí tooltip dựa trên vị trí của phần text
            let rect = textElement.getBoundingClientRect();
            // Cho phép tooltip render để có offsetHeight
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 5}px`;
            tooltip.style.left = `${rect.left + rect.width / 2}px`;
            tooltip.style.transform = "translateX(-50%)";
            tooltip.style.visibility = "visible";

            // Lưu tham chiếu tooltip để có thể xóa khi rời chuột
            textElement._tooltip = tooltip;
        });

        textElement.addEventListener("mouseleave", function () {
            if (textElement._tooltip) {
                textElement._tooltip.remove();
                textElement._tooltip = null;
            }
        });
    });
});
