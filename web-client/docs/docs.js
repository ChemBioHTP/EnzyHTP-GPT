

// Function to convert Markdown to HTML
function markdownToHtml(markdown) {
  let html = markdown;

  // Convert headers
  html = html.replace(/^#\s+(.*$)/gm, ""); // Discard H1
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
const filePath = "./docs/terms_en-us.md"; // Replace with your Markdown file path
fetch(filePath)
  .then((res) => res.text())
  .then((text) => {
    // Convert Markdown content to HTML
    const htmlContent = markdownToHtml(text);

    // Write the HTML content.
    document.getElementById("whitepaper-paragraphs").innerHTML = htmlContent;
  });
