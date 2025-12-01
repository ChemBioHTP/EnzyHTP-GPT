const moduleApi = import.meta.glob('./apis/*.js', { eager: true }) //批量导入
let allModules = {}
for (const path in moduleApi){ //导出对象
  let itemKey = path.replace('./apis/', '').replace('.js', '') //模块名
  allModules[itemKey] = moduleApi[path] //模块内容
}

export default allModules