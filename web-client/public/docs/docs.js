
/**
 * Get Params from HTTP Header.
 * @returns An object containing param name and value as a dictionary.
 */
function GetRequest() {
  var url = location.search; // Get params from http header.
  //   console.log(url);
  var theRequest = new Object();
  if (url.indexOf("?") != -1) {
    var str = url.substr(1);
    strs = str.split("&");
    for (var i = 0; i < strs.length; i++) {
      theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
    }
  }
  //   console.log(theRequest);
  return theRequest;
}

var request = GetRequest();         // A dictionary recording request search information.
let doc = request.doc ?? "terms";    // The document to be displayed.
let lang = request.lang ?? "en-us"; // The language to be displayed.

// console.log(`doc: ${doc}, lang: ${lang}`);

function makeSearch(new_doc = doc, new_lang = lang) {
  location.search = `?doc=${new_doc}&lang=${new_lang}`
}

// Function to convert Markdown to HTML
function markdownToHtml(markdown) {
  let html = markdown;

  // Convert headers
  html = html.replace(/^#\s+(.*$)/gm, "<h2>$1</h2>"); // H1 to <h2>
  html = html.replace(/^##\s+(.*$)/gm, "<h4>$1</h4>"); // H2 to <h4>
  html = html.replace(/^###\s+(.*$)/gm, "<h5>$1</h5>"); // H3 to <h5>

  // Convert paragraphs
  html = html.replace(
    /^(?!<h[45]>|<ul>|<ol>|<li>|<b>)([^\n]+)\n?/gm,
    "<p>$1</p>"
  );

  // Convert bold text
  html = html.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");

  // Convert unordered lists
  html = html.replace(/(^|\n)-\s+(.*)/g, "$1<ul><li>$2</li></ul>");
  html = html.replace(/<\/ul>\s*<ul>/g, ""); // Merge adjacent <ul>

  // Convert ordered lists
  html = html.replace(/(^|\n)\d+\.\s+(.*)/g, "$1<ol><li>$2</li></ol>");
  html = html.replace(/<\/ol>\s*<ol>/g, ""); // Merge adjacent <ol>

  return html;
}

// Read Markdown file
const filePath = `./docs/${doc}_${lang}.md`; // Replace with your Markdown file path
fetch(filePath)
  .then((res) => res.text())
  .then((text) => {
    // Convert Markdown content to HTML
    const htmlContent = markdownToHtml(text);

    // Write the HTML content.
    document.getElementById("paragraphs").innerHTML = htmlContent;
  });
