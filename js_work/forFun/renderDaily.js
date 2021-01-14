/* a part of my blog */
/* for generating contents of daily front-end*/
/* pagination component */

let startDay = 1;
let currentPage = 1;
const dayRange = 3;
const dayNum = 5;

function render(day) {
  async function renderTemplate(jsCode, cssCode, title, height) {
    var temp = document.createElement("div");
    temp.classList = `containter day${day}`;

    var titleEle = document.createElement("h2");
    titleEle.innerHTML = `Day ${day}. ${title}`;

    var effectEle = document.createElement("h3");
    effectEle.innerHTML = "效果";

    var show = document.createElement("div");
    show.classList = "show-effect";
    show.innerHTML = `<iframe align="center" width=100%" height=${height} src="/frontEnd-daily/day${day}/day${day}.html"  frameborder="no" border="0"></iframe>`;

    var codeBlock = document.createElement("div");
    codeBlock.classList = "codeBlock mainCode";

    var jsBlock = document.createElement("div");
    jsBlock.classList = "js-code";
    var h3Js = document.createElement("h3");
    h3Js.innerHTML = "JavaScript";
    var preJs = document.createElement("pre");
    preJs.style = "background-color: #d6cbcb";
    var codeJs = document.createElement("code");
    codeJs.classList = "javascript";
    codeJs.innerHTML = jsCode;

    // jsBlock.appendChild(codeJs)

    var cssBlock = document.createElement("div");
    cssBlock.classList = "css-code";
    var h3Css = document.createElement("h3");
    h3Css.innerHTML = "CSS";
    var preCss = document.createElement("pre");
    preCss.style = "background-color: rgb(173, 166, 166)"; //
    var codeCss = document.createElement("code");
    codeCss.classList = "css";
    codeCss.innerHTML = cssCode;

    preJs.appendChild(codeJs);
    jsBlock.appendChild(h3Js);
    jsBlock.appendChild(preJs);

    preCss.appendChild(codeCss);
    cssBlock.appendChild(h3Css);
    cssBlock.appendChild(preCss);

    codeBlock.appendChild(jsBlock);
    codeBlock.appendChild(cssBlock);

    var note = document.createElement("div");
    note.classList = "summary-note";
    var h3Note = document.createElement("h3");
    h3Note.innerHTML = "小结";
    note.appendChild(h3Note);

    temp.appendChild(titleEle);
    temp.appendChild(effectEle);
    temp.appendChild(show);
    temp.appendChild(codeBlock);
    temp.appendChild(note);

    return temp;
  }

  async function renderCode() {
    var respJS = await fetch(`/frontEnd-daily/day${day}/scriptDay${day}.js`);
    var js = await respJS.text();

    var respCSS = await fetch(`/frontEnd-daily/day${day}/styleDay${day}.css`);
    var css = await respCSS.text();
    try {
      return [js, css];
    } catch (error) {
      alert(error);
    }
  }

  async function renderItem(data) {
    var title = data[day]["title"];
    var height = data[day]["height"];
    var code = await renderCode();
    var temp = await renderTemplate(code[0], code[1], title, height);
    // console.log(temp);
    return temp;
  }
  return renderItem;
}

async function generatePage(startDay, dayRange) {
  var aim = document.querySelector(".container-frontend");

  $(".container-frontend")
    .children()
    .slideUp(500, function () {
      $(this).remove();
    });

  data = await $.getJSON("/frontEnd-daily/dayDate.json");
  var promise = [];
  for (let day = startDay; day <= startDay + dayRange - 1; day++) {
    promise.push(render(day)(data));
  }

  temps = await Promise.all(promise);
  temps.forEach((temp) => aim.append(temp));
  document.querySelectorAll("code").forEach((block) => {
    hljs.highlightBlock(block);
  });
}

// const currentPage = 1

function renderPagniation() {
  var currentPage = 1;
  var pageNum = Math.ceil(dayNum / dayRange);
  var prev = document.querySelector(".page-item.prev");
  var next = document.querySelector(".page-item.next");
  var pagination = document.querySelector(".pagination");

  for (let page = 1; page <= pageNum; page++) {
    var button = document.createElement("button");
    button.classList =
      page === 1 ? ["page-item num active"] : ["page-item num"];
    button.innerHTML = page;
    pagination.insertBefore(button, next);
  }
  var pages = document.querySelectorAll(".page-item.num");

  function update() {
    pages.forEach((ele) => ele.classList.remove("active"));
    pages[currentPage - 1].classList.add("active");
    var left = (currentPage - 1) * dayRange + 1;
    var right = left + dayRange - 1;
    console.log(right);
    right = right <= dayNum ? dayRange : dayRange - (right - dayNum);
    prev.disabled = currentPage === 1;
    next.disabled = currentPage === pages.length;
    console.log([left, right]);
    generatePage(left, right);
    window.scrollTo(0, 0);
  }

  pages.forEach((ele) => {
    ele.addEventListener("click", function () {
      currentPage = parseInt(ele.innerHTML);
      update();
    });
  });

  prev.addEventListener("click", function () {
    currentPage--;
    currentPage = currentPage < 1 ? 1 : currentPage;
    update();
  });

  next.addEventListener("click", function () {
    currentPage++;
    currentPage = currentPage > pages.length ? pages.length : currentPage;
    update();
  });
}

(() => {
  generatePage(1, dayRange);
  renderPagniation();
})();