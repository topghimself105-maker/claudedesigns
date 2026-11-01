// SENTINEL SCAN v2 viewport: cinematic macro close-ups of "the Sentinel core" (no real chart), one object per journal field.
// Pseudo-3D canvas rendering: shaded spheres, tube membranes, bubbles, filaments, depth of field (far + near layers blurred). Seeded, pure function of t.
(function(){
const LW=1032,LH=670,TAU=Math.PI*2;
const mk=()=>{const c=document.createElement('canvas');c.width=LW;c.height=LH;return [c,c.getContext('2d')];};
const [farC,far]=mk(),[midC,mid]=mk(),[nearC,near]=mk();
const h=(a,b)=>{let r=(Math.imul(a|0,374761393)+Math.imul((b|0)+7919,668265263))|0;r=Math.imul(r^(r>>>13),1274126177);r^=r>>>16;return (r>>>0)/4294967296;};
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v)),lerp=(a,b,t)=>a+(b-a)*t,eo=t=>1-Math.pow(1-clamp(t,0,1),3),mod=(v,m)=>((v%m)+m)%m;
// palette (hue/sat/light) so every object can be shaded consistently
const P={deep:[155,80,5],body:[152,70,22],lime:[140,85,55],mint:[155,90,62],teal:[170,80,45],amber:[42,95,58],red:[352,90,62],cyan:[188,85,58]};
const hsl=(c,dl,a)=>`hsla(${c[0]},${c[1]}%,${clamp(c[2]+(dl||0),0,100)}%,${a===undefined?1:a})`;
function sphere(g,x,y,r,c,opt){opt=opt||{};const lx=x-r*.38,ly=y-r*.42;
 const gr=g.createRadialGradient(lx,ly,r*.05,x,y,r);gr.addColorStop(0,hsl(c,32));gr.addColorStop(.35,hsl(c,8));gr.addColorStop(.8,hsl(c,-14));gr.addColorStop(1,hsl(c,-24));g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,TAU);g.fill();
 const rim=g.createRadialGradient(x,y,r*.75,x,y,r);rim.addColorStop(0,'rgba(0,0,0,0)');rim.addColorStop(1,hsl(c,25,.55));g.fillStyle=rim;g.beginPath();g.arc(x,y,r,0,TAU);g.fill();
 if(opt.bumps){const n=opt.bumps;for(let i=0;i<n;i++){const a=h(opt.seed||1,i)*TAU,d=Math.sqrt(h((opt.seed||1)+1,i))*.92,px=x+Math.cos(a)*d*r,py=y+Math.sin(a)*d*r,s=r*(.025+.05*h((opt.seed||1)+2,i))*(1-d*.6);if(s<.6)continue;const bg=g.createRadialGradient(px-s*.3,py-s*.35,0,px,py,s);bg.addColorStop(0,hsl(c,38,.95));bg.addColorStop(1,hsl(c,-6,.0));g.fillStyle=bg;g.beginPath();g.arc(px,py,s,0,TAU);g.fill();}}
 const sp=g.createRadialGradient(lx,ly,0,lx,ly,r*.3);sp.addColorStop(0,'rgba(255,255,255,.55)');sp.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=sp;g.beginPath();g.arc(lx,ly,r*.3,0,TAU);g.fill();}
function glow(g,x,y,r,c,a){const gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,hsl(c,20,a));gr.addColorStop(1,hsl(c,0,0));g.save();g.globalCompositeOperation='lighter';g.fillStyle=gr;g.beginPath();g.arc(x,y,r,0,TAU);g.fill();g.restore();}
// a tube along a path: dark body, lighter core, thin specular line offset up-left
function tube(g,pts,w,c,close){const path=()=>{g.beginPath();pts.forEach((p,i)=>i?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1]));if(close)g.closePath();};g.save();g.lineCap='round';g.lineJoin='round';
 [[1,-18,1],[.8,-6,1],[.55,6,1],[.3,20,.9],[.1,40,.8]].forEach(([k,dl,a],i)=>{g.save();if(i>=3)g.translate(-w*.12,-w*.14);g.strokeStyle=hsl(c,dl,a);g.lineWidth=w*k;path();g.stroke();g.restore();});g.restore();}
function curve(n,f){const o=[];for(let i=0;i<=n;i++)o.push(f(i/n));return o;}
function bubbles(g,t,n,seed,c,area,rise,size){const [x0,y0,w,hh]=area;for(let i=0;i<n;i++){const s=(size||1)*(3+h(seed,i)*16),px=x0+mod(h(seed+1,i)*w+Math.sin(t*.6+i)*12,w),py=y0+mod(h(seed+2,i)*hh-t*(rise||12)*(.5+h(seed+3,i)),hh);
 g.save();g.globalAlpha=.35+.5*h(seed+4,i);g.strokeStyle=hsl(c,30,.7);g.lineWidth=1.2;g.fillStyle=hsl(c,10,.12);g.beginPath();g.arc(px,py,s,0,TAU);g.fill();g.stroke();g.fillStyle='rgba(255,255,255,.7)';g.beginPath();g.arc(px-s*.35,py-s*.35,s*.18,0,TAU);g.fill();g.restore();}}
function filaments(g,t,n,seed,c,a){g.save();g.globalCompositeOperation='lighter';for(let i=0;i<n;i++){const y0=h(seed,i)*LH,y1=h(seed+1,i)*LH,cy=(y0+y1)/2+(h(seed+2,i)-.5)*300+Math.sin(t*.5+i)*20;g.strokeStyle=hsl(c,10,(a||.25)*h(seed+3,i));g.lineWidth=.8+h(seed+4,i)*1.8;g.beginPath();g.moveTo(-20,y0);g.quadraticCurveTo(LW/2,cy,LW+20,y1);g.stroke();}g.restore();}
function dust(g,t,n,seed,c){for(let i=0;i<n;i++){const px=mod(h(seed,i)*LW+t*(5+10*h(seed+1,i)),LW),py=mod(h(seed+2,i)*LH-t*(4+8*h(seed+3,i)),LH),r=.8+h(seed+4,i)*2.2;g.fillStyle=hsl(c,30,.25+.5*h(seed+5,i));g.beginPath();g.arc(px,py,r,0,TAU);g.fill();}}
function bokeh(g,t,n,seed,c){for(let i=0;i<n;i++){const px=mod(h(seed,i)*LW+t*14*(h(seed+1,i)-.5),LW),py=mod(h(seed+2,i)*LH+t*10*(h(seed+3,i)-.5),LH),r=20+h(seed+4,i)*70,gr=g.createRadialGradient(px,py,0,px,py,r);gr.addColorStop(0,hsl(c,20,.18*h(seed+5,i)+.04));gr.addColorStop(.7,hsl(c,10,.06));gr.addColorStop(1,hsl(c,0,0));g.fillStyle=gr;g.beginPath();g.arc(px,py,r,0,TAU);g.fill();}}
function granules(g,t,n,seed,c,area,smin,smax){const [x0,y0,w,hh]=area||[0,0,LW,LH];for(let i=0;i<n;i++){const px=x0+mod(h(seed,i)*w+Math.sin(t*.3+i)*6,w),py=y0+mod(h(seed+1,i)*hh+Math.cos(t*.25+i)*6,hh),r=(smin||4)+h(seed+2,i)*((smax||22)-(smin||4));const cc=h(seed+3,i)<.2?P.mint:(h(seed+3,i)<.5?P.teal:P.body);sphere(g,px,py,r,cc);}}
function bgFill(g,c1,c2){const gr=g.createRadialGradient(LW*.55,LH*.45,40,LW*.5,LH*.5,LW*.75);gr.addColorStop(0,c1);gr.addColorStop(1,c2);g.fillStyle=gr;g.fillRect(0,0,LW,LH);g.save();g.globalAlpha=.55;granules(g,TT,110,(c1.length*97)|0,P.body,[0,0,LW,LH],3,26);g.restore();}
let TT=0;
// --- the cutaway (overview + locator) ---
function cutaway(g,t,cx,cy,s,focus){g.save();g.translate(cx,cy);g.scale(s,s);
 // membrane
 const mem=curve(120,u=>{const a=u*TAU;return [Math.cos(a)*(430+14*Math.sin(a*5+t*.4)),Math.sin(a)*(275+10*Math.cos(a*4))];});
 g.fillStyle='rgba(4,40,28,.85)';g.beginPath();mem.forEach((p,i)=>i?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1]));g.fill();tube(g,mem,30,P.body,true);
 const inner=g.createRadialGradient(0,0,40,0,0,430);inner.addColorStop(0,'rgba(60,245,160,.18)');inner.addColorStop(1,'rgba(60,245,160,0)');g.fillStyle=inner;g.beginPath();g.ellipse(0,0,410,260,0,0,TAU);g.fill();
 g.save();g.beginPath();g.ellipse(0,0,405,255,0,0,TAU);g.clip();for(let i=0;i<70;i++){const a=h(201,i)*TAU,d=Math.sqrt(h(202,i))*.95;sphere(g,Math.cos(a)*d*400,Math.sin(a)*d*250,4+h(203,i)*14,h(204,i)<.3?P.mint:P.teal,{bumps:6,seed:i});}g.strokeStyle='rgba(124,255,196,.18)';g.lineWidth=1.2;for(let i=0;i<40;i++){g.beginPath();g.moveTo(Math.cos(h(205,i)*TAU)*400,Math.sin(h(205,i)*TAU)*250);g.quadraticCurveTo((h(206,i)-.5)*300,(h(207,i)-.5)*200,Math.cos(h(208,i)*TAU)*400,Math.sin(h(208,i)*TAU)*250);g.stroke();}g.restore();
 // modules (positions shared with the locator)
 const M=MODS;
 tube(g,curve(30,u=>[M.flow[0]-120+u*240,M.flow[1]+Math.sin(u*6)*16]),26,P.teal);
 [0,1,2,3].forEach(k=>tube(g,curve(24,u=>[M.dol[0]-90+u*180,M.dol[1]-40+k*22+Math.sin(u*3.2)*18]),14,P.lime));
 for(let k=0;k<12;k++){const a=k/12*TAU;sphere(g,M.toi[0]+Math.cos(a)*62,M.toi[1]+Math.sin(a)*30,12,k===3?P.mint:P.body);}
 sphere(g,M.smt[0]-26,M.smt[1],30,P.mint,{bumps:30,seed:3});sphere(g,M.smt[0]+30,M.smt[1]-8,26,P.cyan,{bumps:24,seed:4});
 sphere(g,M.poi[0],M.poi[1],40,P.lime,{bumps:30,seed:5});sphere(g,M.sweep[0],M.sweep[1],34,P.teal,{bumps:20,seed:6});
 sphere(g,M.ote[0],M.ote[1],30,P.mint,{bumps:20,seed:7});sphere(g,M.inval[0],M.inval[1],26,P.red,{bumps:12,seed:8});sphere(g,M.target[0],M.target[1],24,P.amber,{bumps:12,seed:9});
 sphere(g,M.news[0],M.news[1],95,P.mint,{bumps:90,seed:10});glow(g,M.news[0],M.news[1],180,P.mint,.25);
 if(focus){const f=M[focus];if(f){g.strokeStyle='rgba(227,255,241,.95)';g.lineWidth=5;g.beginPath();g.arc(f[0],f[1],90,0,TAU);g.stroke();}}
 g.restore();}
const MODS={news:[0,-10],flow:[-230,120],dol:[-200,-120],sweep:[150,150],poi:[260,40],toi:[-60,190],smt:[200,-150],ote:[330,-40],inval:[60,215],target:[-330,0],order:[0,-10]};
// --- scene per shot (draws into far / mid / near) ---
const SC={
 overview(t,lt){bgFill(far,'#05301F','#000805');filaments(far,t,24,1,P.teal,.35);dust(far,t,90,2,P.mint);cutaway(mid,t,LW/2,LH/2+10,1.16);bubbles(near,t,10,3,P.mint,[0,0,LW,LH],10,2.2);},
 news(t,lt){bgFill(far,'#073A26','#000805');filaments(far,t,20,11,P.amber,.18);dust(far,t,80,12,P.mint);
  const cx=LW*.56,cy=LH*.52,R=260;glow(mid,cx,cy,R*1.6,P.amber,.18);sphere(mid,cx,cy,R,P.body,{bumps:260,seed:13});
  // cut-out showing the glowing inner core
  mid.save();mid.beginPath();mid.ellipse(cx+40,cy+30,R*.62,R*.55,-.3,0,TAU);mid.clip();mid.fillStyle='#021309';mid.fillRect(0,0,LW,LH);sphere(mid,cx+48,cy+40,R*.36,P.amber,{bumps:80,seed:14});glow(mid,cx+48,cy+40,R*.7,P.amber,.5);mid.restore();
  mid.save();mid.strokeStyle=hsl(P.mint,20,.9);mid.lineWidth=10;mid.beginPath();mid.ellipse(cx+40,cy+30,R*.62,R*.55,-.3,0,TAU);mid.stroke();mid.restore();
  for(let r=0;r<3;r++){const e=mod(lt*.7+r/3,1);mid.strokeStyle=hsl(P.amber,20,.55*(1-e));mid.lineWidth=3;mid.beginPath();mid.arc(cx+48,cy+40,R*.4+e*420,0,TAU);mid.stroke();}
  bubbles(near,t,12,15,P.mint,[0,0,LW,LH],14,2.4);},
 flow(t,lt){bgFill(far,'#04301F','#000805');filaments(far,t,30,21,P.teal,.3);
  const wall=(off,c)=>tube(mid,curve(60,u=>[-60+u*(LW+120),LH*.5+off-u*220+Math.sin(u*7+t*.6)*18]),70,c);wall(-170,P.body);wall(190,P.body);
  for(let i=0;i<60;i++){const u=mod(h(22,i)+lt*.32,1),px=-40+u*(LW+80),py=LH*.5-u*220+(h(23,i)-.5)*260,r=6+h(24,i)*18;sphere(mid,px,py,r,h(25,i)<.3?P.mint:P.lime);}
  glow(mid,LW*.75,LH*.25,260,P.mint,.25);bubbles(near,t,8,26,P.mint,[0,0,LW,LH],30,2.6);},
 dol(t,lt){bgFill(far,'#05351F','#000805');dust(far,t,120,31,P.amber);
  const cx=LW*.5,cy=LH*.2;// liquidity pool (glossy droplet surface) above
  const pg=mid.createLinearGradient(0,cy-120,0,cy+120);pg.addColorStop(0,hsl(P.amber,25,.95));pg.addColorStop(.5,hsl(P.amber,-5,.9));pg.addColorStop(1,hsl(P.amber,-25,.9));mid.fillStyle=pg;mid.beginPath();mid.ellipse(cx,cy,LW*.55,130,0,0,TAU);mid.fill();
  for(let k=0;k<6;k++){const e=mod(lt*.5+k/6,1);mid.strokeStyle=`rgba(255,240,200,${.5*(1-e)})`;mid.lineWidth=2;mid.beginPath();mid.ellipse(cx,cy,40+e*LW*.5,10+e*120,0,0,TAU);mid.stroke();}
  for(let i=0;i<70;i++){const u=mod(h(32,i)+lt*.4,1),px=cx+(h(33,i)-.5)*LW*.9*(1-u*.5),py=LH+20-u*(LH-cy),r=3+h(34,i)*12;sphere(mid,px,py,r,P.lime);}
  glow(mid,cx,cy,400,P.amber,.25);bubbles(near,t,8,35,P.amber,[0,0,LW,LH],20,2.4);},
 sweep(t,lt){bgFill(far,'#04301F','#000805');filaments(far,t,24,41,P.teal,.3);
  const y=LH*.52;for(let k=0;k<5;k++)tube(mid,curve(50,u=>[-40+u*(LW+80),y-60+k*30+Math.sin(u*6+k)*6]),26-k*2,k%2?P.body:P.teal);
  const tip=LH*.52+130+20*Math.sin(lt*3),sx=LW*.5;const sg=mid.createLinearGradient(sx-50,0,sx+50,0);sg.addColorStop(0,hsl(P.mint,-20));sg.addColorStop(.5,hsl(P.mint,25));sg.addColorStop(1,hsl(P.mint,-25));mid.fillStyle=sg;mid.beginPath();mid.moveTo(sx-56,-20);mid.lineTo(sx+56,-20);mid.lineTo(sx,tip);mid.closePath();mid.fill();
  for(let i=0;i<50;i++){const e=mod(lt*.9+h(42,i),1),a=h(43,i)*TAU,r=e*260*(.3+h(44,i));sphere(mid,sx+Math.cos(a)*r,tip-20+Math.sin(a)*r*.5,3+5*(1-e),P.mint);}
  glow(mid,sx,tip,240,P.mint,.45);bubbles(near,t,8,45,P.mint,[0,0,LW,LH],14,2.4);},
 poi(t,lt){bgFill(far,'#06381F','#000805');dust(far,t,90,51,P.lime);
  const gap=[LH*.42,LH*.6];const slab=(y0,y1,c)=>{const g=mid.createLinearGradient(0,y0,0,y1);g.addColorStop(0,hsl(c,10));g.addColorStop(1,hsl(c,-18));mid.fillStyle=g;mid.beginPath();mid.moveTo(-20,y0);for(let i=0;i<=20;i++)mid.lineTo(i*LW/20,y0+Math.sin(i*1.3)*8);mid.lineTo(LW+20,y1);mid.lineTo(-20,y1);mid.fill();};
  slab(-40,gap[0],P.body);slab(gap[1],LH+40,P.body);granules(mid,t,60,57,P.body,[0,0,LW,gap[0]-14],4,18);granules(mid,t,60,58,P.body,[0,gap[1]+14,LW,LH-gap[1]],4,18);tube(mid,curve(40,u=>[-20+u*(LW+40),gap[0]]),16,P.teal);tube(mid,curve(40,u=>[-20+u*(LW+40),gap[1]]),16,P.teal);
  const gg=mid.createLinearGradient(0,gap[0],0,gap[1]);gg.addColorStop(0,'rgba(124,255,196,.05)');gg.addColorStop(.5,'rgba(124,255,196,.55)');gg.addColorStop(1,'rgba(124,255,196,.05)');mid.fillStyle=gg;mid.fillRect(0,gap[0]+8,LW,gap[1]-gap[0]-16);
  for(let i=0;i<14;i++){const px=mod(h(52,i)*LW+lt*30*(h(53,i)-.3),LW),py=lerp(gap[0]+30,gap[1]-30,h(54,i)),s=10+h(55,i)*22;mid.save();mid.translate(px,py);mid.rotate(lt*.6+i);const cg=mid.createLinearGradient(-s,-s,s,s);cg.addColorStop(0,hsl(P.mint,30));cg.addColorStop(1,hsl(P.teal,-10));mid.fillStyle=cg;mid.beginPath();mid.moveTo(0,-s);mid.lineTo(s*.6,0);mid.lineTo(0,s);mid.lineTo(-s*.6,0);mid.closePath();mid.fill();mid.restore();}
  glow(mid,LW/2,(gap[0]+gap[1])/2,420,P.mint,.3);bubbles(near,t,8,56,P.lime,[0,0,LW,LH],12,2.4);},
 toi(t,lt){bgFill(far,'#04301F','#000805');filaments(far,t,20,61,P.teal,.25);
  const cx=LW/2,cy=LH*.55,R=330,lit=3;for(let k=0;k<12;k++){const a=k/12*TAU-Math.PI/2+lt*.12,px=cx+Math.cos(a)*R,py=cy+Math.sin(a)*R*.42,s=1-.35*(Math.sin(a)*.5+.5)*0;const on=k===lit;
   for(let d=0;d<6;d++){const g=mid.createLinearGradient(px-40,0,px+40,0);const c=on?P.mint:P.body;g.addColorStop(0,hsl(c,-15));g.addColorStop(.5,hsl(c,on?25:8));g.addColorStop(1,hsl(c,-20));mid.fillStyle=g;mid.beginPath();mid.ellipse(px,py-d*12,44,14,0,0,TAU);mid.fill();mid.strokeStyle=hsl(c,30,.6);mid.lineWidth=1;mid.stroke();}
   if(on)glow(mid,px,py-30,140,P.mint,.55);}
  mid.strokeStyle='rgba(227,255,241,.8)';mid.lineWidth=4;const a=3/12*TAU-Math.PI/2+lt*.12;mid.beginPath();mid.moveTo(cx,cy);mid.lineTo(cx+Math.cos(a)*R*.9,cy+Math.sin(a)*R*.38);mid.stroke();sphere(mid,cx,cy,26,P.mint);bubbles(near,t,8,62,P.mint,[0,0,LW,LH],12,2.2);},
 smt(t,lt){bgFill(far,'#04301F','#000805');dust(far,t,90,71,P.cyan);filaments(far,t,18,72,P.cyan,.2);
  const tr=(c,y0,dip,off)=>{tube(mid,curve(60,u=>[40+u*(LW-80),y0+Math.sin(u*TAU*1.5+off)*40+(u>.55&&u<.8?dip*Math.sin((u-.55)/.25*Math.PI):0)]),6,c);};tr(P.mint,LH*.36,70,0);tr(P.cyan,LH*.7,-35,0);
  sphere(mid,LW*.68,LH*.36+60,70,P.mint,{bumps:70,seed:73});sphere(mid,LW*.68,LH*.7-30,64,P.cyan,{bumps:60,seed:74});
  mid.save();mid.setLineDash([6,8]);mid.strokeStyle='rgba(227,255,241,.7)';mid.lineWidth=2;mid.beginPath();mid.moveTo(LW*.68,LH*.36+130);mid.lineTo(LW*.68,LH*.7-94);mid.stroke();mid.restore();bubbles(near,t,8,75,P.cyan,[0,0,LW,LH],12,2.2);},
 ote(t,lt){bgFill(far,'#04301F','#000805');dust(far,t,100,81,P.mint);
  const cx=LW*.5,cy=LH*.52;for(let k=9;k>=0;k--){const r=60+k*42,band=k>=4&&k<=6;mid.strokeStyle=band?hsl(P.mint,25,.95):hsl(P.teal,-5,.55);mid.lineWidth=band?10:3;mid.beginPath();mid.ellipse(cx,cy,r*1.5,r*.55,0,0,TAU);mid.stroke();}
  const bg=mid.createRadialGradient(cx,cy,0,cx,cy,380);bg.addColorStop(0,'rgba(124,255,196,.35)');bg.addColorStop(1,'rgba(124,255,196,0)');mid.fillStyle=bg;mid.beginPath();mid.ellipse(cx,cy,560,210,0,0,TAU);mid.fill();
  sphere(mid,cx,cy-120+Math.sin(lt*2)*6,46,P.mint,{bumps:40,seed:82});mid.strokeStyle='rgba(227,255,241,.8)';mid.lineWidth=2;mid.beginPath();mid.moveTo(cx,cy-74);mid.lineTo(cx,cy);mid.stroke();glow(mid,cx,cy,120,P.mint,.6);bubbles(near,t,8,83,P.mint,[0,0,LW,LH],12,2.2);},
 inval(t,lt){bgFill(far,'#04301F','#000805');dust(far,t,80,91,P.red);
  const y0=LH*.62;for(let r=0;r<4;r++)for(let k=-1;k<14;k++){const px=k*86+(r%2)*43-mod(lt*10,86),py=y0+r*46,s=1+r*.18;mid.save();mid.translate(px,py);mid.scale(s,s*.42);mid.beginPath();for(let i=0;i<6;i++){const a=i/6*TAU;mid.lineTo(Math.cos(a)*44,Math.sin(a)*44);}mid.closePath();const g=mid.createLinearGradient(0,-44,0,44);g.addColorStop(0,hsl(P.body,12));g.addColorStop(1,hsl(P.deep,0));mid.fillStyle=g;mid.fill();mid.strokeStyle=hsl(P.red,0,.75);mid.lineWidth=3;mid.stroke();mid.restore();}
  glow(mid,LW/2,y0,500,P.red,.18);granules(mid,t,40,94,P.body,[0,0,LW,y0-120],5,20);sphere(mid,LW/2,y0-110+6*Math.sin(lt*3),70,P.mint,{bumps:60,seed:92});bubbles(near,t,8,93,P.red,[0,0,LW,LH],12,2.2);},
 target(t,lt){bgFill(far,'#04301F','#000805');dust(far,t,110,101,P.amber);
  const sx=LW*.6;const bg=mid.createLinearGradient(sx-60,0,sx+60,0);bg.addColorStop(0,'rgba(255,200,87,0)');bg.addColorStop(.5,'rgba(255,220,140,.55)');bg.addColorStop(1,'rgba(255,200,87,0)');mid.fillStyle=bg;mid.fillRect(sx-60,0,120,LH);
  const sp=mid.createLinearGradient(sx-70,0,sx+70,0);sp.addColorStop(0,hsl(P.teal,-20));sp.addColorStop(.5,hsl(P.mint,22));sp.addColorStop(1,hsl(P.teal,-25));mid.fillStyle=sp;mid.beginPath();mid.moveTo(sx-80,LH+20);mid.lineTo(sx-18,LH*.25);mid.lineTo(sx,LH*.12);mid.lineTo(sx+18,LH*.25);mid.lineTo(sx+80,LH+20);mid.closePath();mid.fill();
  mid.strokeStyle=hsl(P.amber,20,.9);mid.lineWidth=5;mid.beginPath();mid.ellipse(sx,LH*.1,150,26,0,0,TAU);mid.stroke();glow(mid,sx,LH*.1,300,P.amber,.45);
  for(let i=0;i<40;i++){const u=mod(h(102,i)+lt*.5,1),px=sx+(h(103,i)-.5)*220,py=LH-u*LH*.9;sphere(mid,px,py,2+h(104,i)*5,P.amber);}bubbles(near,t,8,105,P.amber,[0,0,LW,LH],18,2.2);},
 order(t,lt){bgFill(far,'#073A26','#000805');filaments(far,t,26,111,P.mint,.3);dust(far,t,90,112,P.mint);
  const cx=LW*.32,cy=LH*.5,R=210;glow(mid,cx,cy,R*1.8,P.mint,.25+.25*FILLK(t));sphere(mid,cx,cy,R,P.body,{bumps:220,seed:113});mid.save();mid.beginPath();mid.arc(cx+30,cy+20,R*.55,0,TAU);mid.clip();mid.fillStyle='#021309';mid.fillRect(0,0,LW,LH);sphere(mid,cx+36,cy+26,R*.32,P.mint,{bumps:60,seed:114});glow(mid,cx+36,cy+26,R*.7,P.mint,.6);mid.restore();
  const f=FILLK(t);for(let r=0;r<4;r++){const e=clamp(f*1.3-r*.15,0,1);if(e>0&&e<1){mid.strokeStyle=`rgba(200,255,225,${1-e})`;mid.lineWidth=4;mid.beginPath();mid.arc(cx+36,cy+26,R*.3+e*700,0,TAU);mid.stroke();}}bubbles(near,t,10,115,P.mint,[0,0,LW,LH],16,2.4);}
};
let FILLT=1e9;const FILLK=t=>t<FILLT?0:clamp((t-FILLT)/1.2,0,1);
// public: render shot k at time t into ctx at (vx,vy), camera push z
window.SCENE={MODS,render(ctx,vx,vy,k,t,lt,z,fillT){FILLT=fillT;TT=t;[far,mid,near].forEach(g=>{g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,LW,LH);});
 const cam=(g,zz,rot)=>{g.setTransform(1,0,0,1,0,0);g.translate(LW/2,LH/2);g.scale(zz,zz);g.rotate(rot);g.translate(-LW/2,-LH/2);};
 cam(far,1+(z-1)*.4,0);cam(mid,z,(z-1)*.08);cam(near,1+(z-1)*1.8,0);(SC[k]||SC.overview)(t,lt);
 ctx.save();ctx.filter='blur(5px)';ctx.drawImage(farC,vx,vy);ctx.filter='none';ctx.drawImage(midC,vx,vy);ctx.filter='blur(7px)';ctx.drawImage(nearC,vx,vy);ctx.filter='none';ctx.restore();},
 locator(ctx,x0,y0,w,hh,focus,t){ctx.save();ctx.beginPath();ctx.rect(x0,y0,w,hh);ctx.clip();ctx.fillStyle='#021309';ctx.fillRect(x0,y0,w,hh);cutaway(ctx,0,x0+w/2,y0+hh/2,Math.min(w/900,hh/580),focus);ctx.restore();}};
})();
