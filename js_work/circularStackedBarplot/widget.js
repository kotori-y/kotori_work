/*
 * @Description:
 * @Author: Kotori Y
 * @Date: 2021-06-05 16:33:14
 * @LastEditors: Kotori Y
 * @LastEditTime: 2021-06-05 16:33:15
 * @FilePath: \ddiDatabase0603\widget.js
 * @AuthorMail: kotori@cbdd.me
 */
document.getElementById("colorMap").value =
  "#547da7\r\n#678eb5\r\n#7a9fc4\r\n#8db0d2\r\n#a1c1e1\r\n#b5d3f0\r\n#c9e5ff";
// "#15546d\r\n#346b84\r\n#4f839b\r\n#699bb3\r\n#84b4cc\r\n#9fcee5\r\n#bae9ff";

document.querySelector("#hidden").addEventListener("click", () => {
  document.querySelector(".container").style.display = "none";
  alert("Pressing Key D to display color config area!");
});

document.addEventListener("keydown", (e) => {
  if (e.code === "KeyD") {
    document.querySelector(".container").style.display = "block";
  }
});
