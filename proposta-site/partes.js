// Cabeçalho e rodapé comuns a todas as telas da proposta.
(function () {
  var LOJA = 'https://www.simlivraria.com.br/';
  var ativo = document.body.getAttribute('data-ativo') || '';
  var itens = [
    ['inicio', 'Início', 'index.html'],
    ['eventos', 'Eventos', 'eventos.html'],
    ['cursos', 'Cursos', 'cursos.html'],
    ['formacao', 'Formação', 'formacao.html'],
    ['loja', 'Loja', LOJA],
    ['oracao', 'Pedido de Oração', 'oracao.html']
  ];
  var menu = itens.map(function (i) {
    var ext = i[2].indexOf('http') === 0 ? ' target="_blank" rel="noopener"' : '';
    return '<li><a class="' + (i[0] === ativo ? 'ativo' : '') + '" href="' + i[2] + '"' + ext + '>' + i[1] + '</a></li>';
  }).join('');
  document.body.insertAdjacentHTML('afterbegin',
    '<div class="topbar"><div class="wrap"><span>✦ <b>Ano Jubilar</b> · 30 anos de história e missão · 1996–2026</span><span class="esc">WhatsApp <b>(18) 99670-8825</b> · <b>@sim_dracena</b></span></div></div>' +
    '<header class="nav"><div class="wrap"><a class="marca" href="index.html"><img src="../site/img/logo-sim.jpg" alt=""><span><b>Comunidade SIM</b><small>Irmãos da Misericórdia</small></span></a>' +
    '<ul class="menu">' + menu + '<li><a class="btn btn-ouro' + (ativo === 'socio' ? ' ativo-btn' : '') + '" href="socio.html">Seja sócio</a></li></ul>' +
    '<span class="hamb"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg></span></div></header>');
  document.body.insertAdjacentHTML('beforeend',
    '<footer><div class="wrap"><div class="grade">' +
    '<div><a class="marca" href="index.html"><img src="../site/img/logo-sim.jpg" alt=""><span><b>Comunidade SIM</b><small>Irmãos da Misericórdia</small></span></a><p class="lema">Jesus, eu confio em vós!</p><div class="redes"><span>IG</span><span>YT</span><span>FB</span><span>WA</span></div></div>' +
    '<div><h4>A comunidade</h4><ul><li><a href="index.html#historia">Nossa história</a></li><li><a href="eventos.html">Eventos</a></li><li><a href="' + LOJA + '" target="_blank" rel="noopener">Loja SIM</a></li><li><a href="socio.html">Seja sócio</a></li></ul></div>' +
    '<div><h4>Cursos e formação</h4><ul><li><a href="cursos.html">Diga SIM a Deus</a></li><li><a href="cursos.html">Santificai-vos</a></li><li><a href="formacao.html">Formação: Igreja, Bíblia e Catecismo</a></li><li><a href="oracao.html">Pedido de oração</a></li></ul></div>' +
    '<div><h4>Contato</h4><ul><li>Rua Spinard, 23</li><li>Jd. Vera Cruz · Dracena-SP</li><li>(18) 99670-8825</li><li>@sim_dracena</li></ul></div>' +
    '</div><p class="copy">© 1996–2026 Sociedade Irmãos da Misericórdia · Ano Jubilar 30 anos</p></div></footer>');
})();
