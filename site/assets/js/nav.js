// 构建统一导航栏，自动高亮当前页面
(function(){
  const pages=[
    ['index.html','首页'],['wake.html','尾流'],['optimization.html','优化'],
    ['overview.html','总览'],['3d_surface.html','3D曲面'],['3d_volume.html','3D体'],
    ['heatmap.html','热力矩阵'],['solver.html','求解器'],['pod.html','POD'],
    ['array.html','阵列'],['power_tracking.html','功率跟踪'],
    ['dashboard.html','Dashboard'],['windrose.html','风玫瑰'],
    ['model.html','模型精度'],['interface.html','接口']
  ];
  const current=location.pathname.split('/').pop()||'index.html';
  // Find the first <nav> on the page and replace its links
  document.querySelectorAll('.nav-links').forEach(function(el){
    el.innerHTML=pages.map(function(p){
      const cls=p[0]===current?' class="active"':'';
      return '<a href="'+p[0]+'"'+cls+'>'+p[1]+'</a>';
    }).join('');
  });
})();
