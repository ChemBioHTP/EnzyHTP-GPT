export const downloadFile = (res, fileName = "downloaded-file.zip") => {
  const blob = new Blob([res], { type: "application/zip" });
  // 创建一个 URL 对象
  const url = URL.createObjectURL(blob);
  // 创建一个虚拟链接元素
  const link = document.createElement("a");
  link.href = url;
  // 设置下载文件的文件名（可选）
  link.download = fileName; // 替换为实际的文件名和扩展名
  // 触发点击下载
  link.click();
  // 释放 URL 对象
  window.URL.revokeObjectURL(url);
};
