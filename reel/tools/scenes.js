/* time shift: each section keeps its own local clock; SH maps it onto the reel */
let SH=0;
const sfx=(k,t,g=1)=>EV.push({kind:k,t:+(t+SH).toFixed(3),gain:g});
const on=f=>{const s=SH;UP.push(t=>f(t-s))};
const END=31.0;

/* ---------------- text helpers ---------------- */
function typeOn(el,t,st,cps=34){const f=el.dataset.full??(el.dataset.full=el.textContent);el.textContent=f.slice(0,Math.floor(cl((t-st)*cps,0,f.length)))}
function radio(par,x,y,who,msg,t0,t1){
  const r=div(par,"radio",`left:${x}px;top:${y}px`,`<div class="rl">● TEAM RADIO</div><div class="rw">${who}</div><div class="rm"></div><div class="wv">${"<i></i>".repeat(28)}</div>`);
  const rm=r.querySelector(".rm"),bars=[...r.querySelectorAll(".wv i")];
  const words=msg.split(" "),a=t0+.4,b=t1-.45;
  sfx("pop",t0,1);
  on(t=>{const vin=oE(P(t,t0,t0+.35)),vout=iC(P(t,t1-.25,t1));
    r.style.opacity=t>=t0&&t<t1?vin*(1-vout):0;r.style.transform=`translateX(${(1-vin)*-60+vout*40}px)`;
    const n=t<a?0:Math.min(words.length,1+Math.floor(P(t,a,b)*words.length));
    rm.textContent=`“${words.slice(0,n).join(" ")}${n>=words.length?"”":""}`;
    const talk=t>=a&&t<b+.05;
    bars.forEach((e,i)=>{const v=talk?Math.abs(Math.sin(t*21+i*1.7)*Math.sin(t*6.3+i*.55))*.9+.1:.08;e.style.height=(v*44).toFixed(1)+"px"})});
}

/* ---------------- S1: construction → full lockup ---------------- */
const LW=880,LS=LW/261.8,LX=100,LY=640,LH=100*LS;
{
  const g=$("#g1");
  const lines=[[LY,"CAP",.1],[LY+LH,"BASE",.25],[LY+LH*.618,"1/φ · 0.618",.4],[LY+LH*.382,"",.55]];
  lines.forEach(([y,lab,st],i)=>{
    const l=mk("line",{x1:0,x2:1080,y1:y,y2:y,stroke:i===2?SKY:ICE,"stroke-opacity":i===2?.8:.28,"stroke-width":1.4,"stroke-dasharray":i===2?"8 8":""},g);
    const tx=mk("text",{x:40,y:y-14,fill:i===2?SKY:STEEL,"font-family":"JBM","font-size":18,"letter-spacing":2},g);tx.textContent=lab;
    sfx("note",st,i);
    on(t=>{const p=ioC(P(t,st,st+.5));const out=1-P(t,2.9,3.4);l.setAttribute("x2",1080*p);l.style.opacity=out;tx.style.opacity=P(t,st+.3,st+.6)*out});
  });
  for(let i=0;i<9;i++){const x=40+i*130;const st=.5+i*.04;
    const l=mk("line",{x1:x,y1:1920,x2:x+1920*K,y2:0,stroke:ICE,"stroke-opacity":.09},g);
    on(t=>{const p=ioC(P(t,st,st+.6));l.setAttribute("x2",x+1920*K*p);l.setAttribute("y2",1920-1920*p);l.style.opacity=1-P(t,2.9,3.4)})}
  const lab12=mk("text",{x:LX+LW-40,y:LY-30,fill:SKY,"font-family":"JBM","font-size":20},g);lab12.textContent="12°";
  on(t=>lab12.style.opacity=P(t,.8,1.0)*(1-P(t,2.9,3.4)));
  const mg=mk("g",{transform:`translate(${LX} ${LY}) scale(${LS})`},g);
  const defs=mk("defs",{},g);
  const ops=[1,.58,.28];
  LOGO.bars.forEach((d,i)=>{
    const cp=mk("clipPath",{id:"bc"+i},defs);const r=mk("rect",{x:-60,width:400,y:100,height:0},cp);
    mk("path",{d,fill:BLUE,"fill-opacity":ops[i],"clip-path":`url(#bc${i})`},mg);
    const st=1.15+(2-i)*.18;
    on(t=>{const q=oE(P(t,st,st+.4));r.setAttribute("y",100-104*q);r.setAttribute("height",104*q)});
  });
  const body=mk("path",{d:LOGO.body,fill:ICE,"fill-opacity":0,stroke:ICE,"stroke-width":1.6/LS,"fill-rule":"evenodd"},mg);
  /* wordmark + hairline + chequer from the lockup, same units as the mark */
  const wcp=mk("clipPath",{id:"wcp"},defs);const wr=mk("rect",{x:-20,y:104,width:0,height:90},wcp);
  const word=mk("g",{"clip-path":"url(#wcp)"},mg);word.innerHTML=LOGO.lockup.slice(LOGO.lockup.indexOf("<g transform"));
  let BL=0;
  on(t=>{if(!BL){BL=body.getTotalLength();body.style.strokeDasharray=BL}
    body.style.strokeDashoffset=BL*(1-ioC(P(t,1.5,2.3)));
    body.setAttribute("fill-opacity",oC(P(t,2.3,2.65)));
    wr.setAttribute("width",320*ioC(P(t,2.55,3.15)));
    word.setAttribute("transform",`translate(${(1-oE(P(t,2.55,3.3)))*-6} 0)`);
    const z=P(t,3.85,4.4);mg.setAttribute("transform",`translate(${LX-z*60} ${LY}) scale(${LS})`);
    g.style.transform=`scale(${1+iC(z)*.25})`;g.style.transformOrigin="50% 50%";g.style.filter=z>0?`blur(${z*10}px)`:"";g.style.opacity=1-iC(z)});
  sfx("riser",.75,1);sfx("hit",2.3,1);sfx("tick",2.6,.5);sfx("thock",4.3,.8);
}
/* pixel transitions */
{const pix=$("#pix");const cells=[];const B=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]];
 for(let j=0;j<32;j++)for(let i=0;i<18;i++){const d=div(pix,"",`left:${i*60}px;top:${j*60}px;background:${(i*7+j*3)%5?BLUE:ICE}`);
  cells.push([d,B[j%4][i%4]/16*.7+(Math.abs(i-9)/9)*.3])}
 const PT=[[4.0,4.3,4.6],[21.0,21.25,21.55]];
 on(t=>{let cov=0;for(const [a,m,b] of PT){if(t>=a&&t<b)cov=t<m?P(t,a,m):1-P(t,m,b)}
  cells.forEach(([d,r])=>d.style.opacity=r<cov?.85:0)});}

SH=-3.15;
/* ---------------- S2: hello — kinetic type ---------------- */
{const w=$("#s2w");const F=96;
 const kick=div(w,"abs k",`left:90px;top:680px;font-size:22px;color:${SKY}`,"Lap zero");
 const L1=div(w,"abs h",`left:90px;top:740px;font-size:${F}px`,"<span class='line' data-split>HEY, I'M AKKI.</span>");
 const L2=div(w,"abs h",`left:90px;top:920px;font-size:${F}px;color:${STEEL}`,"<span class='line' data-split>I'VE RACED IN</span>");
 const sw=div(w,"abs h",`left:90px;top:1012px;font-size:${F}px;height:${F*1.06}px;width:900px;overflow:hidden;color:${BLUE}`,"");
 const WS=["SIM RACING.","KARTING.","FORMULA STUDENT."].map(x=>div(sw,"abs",`left:0;top:0;padding-top:.04em;font-size:${x.length>8?F*.86:F}px`,x));
 const L3=div(w,"abs h",`left:90px;top:1200px;font-size:${F}px;color:${STEEL}`,"<span class='line' data-split>AND I SHOW</span>");
 const L4=div(w,"abs h",`left:90px;top:1292px;font-size:${F}px`,"<span class='line' data-split>YOU HOW.</span>");
 const bar=div(w,"abs",`left:90px;top:1440px;height:4px;width:0;background:${BLUE}`);
 [L1,L2,L3,L4].forEach(split);
 const SW=[8.45,8.95,9.45];
 sfx("tick",7.75,.5);SW.slice(1).forEach(s=>sfx("tick",s,.45));sfx("thock",9.95,.7);sfx("thock",10.95,.8);
 on(t=>{kick.style.opacity=P(t,7.6,7.9);rise(L1,t,7.7,.03);rise(L2,t,8.25,.04);rise(L3,t,9.75,.03);rise(L4,t,9.95,.035);
  WS.forEach((e,i)=>{const a=oE(P(t,SW[i],SW[i]+.32)),b=i<2?oE(P(t,SW[i+1],SW[i+1]+.32)):0;e.style.transform=`translateY(${(1-a)*110-b*110}%)`});
  bar.style.width=380*ioC(P(t,10.2,10.7))+"px";
  const o=iC(P(t,10.7,11.0));w.style.transform=`translateY(${-o*120}px)`;w.style.opacity=1-o});}

/* ---------------- S4: SIM ---------------- */
SH=-1.3;
{const w=$("#s4w");const bg=div(w,"abs","inset:-80px;background:url(assets/06-rails-overlay.png) center/cover;opacity:.22");on(t=>bg.style.transform=`translateX(${-(t-9)*12}px)`);
 const T=title(w,90,150,130,["BUILT ON","THE RIG."],"01 · Sim racing","rigs · grids · racecraft");
 const H=1060,off=H*K,vis=400,g=14,x0=(1080-(3*vis+2*g+off))/2;
 const S=[["williams.jpg","50% 62%","THE GRID"],["coach-booth.jpg","50% 50%","THE COACHING"],["rig.jpg","50% 55%","THE RIG"]]
  .map(([s,pos,lab],i)=>{const p=panel(w,s,x0+i*(vis+g),560,vis+off,H,pos);div(p.o,"cap",`right:${off+28}px;bottom:28px;font-size:16px`,lab);return p});
 on(t=>{slideIn(T.h,t,9.35);T.k.style.opacity=P(t,9.3,9.6);T.s.style.opacity=1;typeOn(T.s,t,9.9);
  S.forEach((p,i)=>{reveal(p,t,9.55+i*.16,.6,-1);p.o.style.transform=`translateY(${(i-1)*(t-9.5)*-4}px)`});
  const x=iC(P(t,13.6,13.95));w.style.transform=`translateX(${-x*1200}px)`;w.style.filter=x>0?`blur(${x*12}px)`:""});
 sfx("thock",13.92,.8);}

/* ---------------- S5: TARMAC (diagonal bands) ---------------- */
{const w=$("#s5w");const bg=div(w,"abs","inset:-80px;background:url(assets/04-speed-lines-overlay.png) center/cover;opacity:.35");on(t=>bg.style.transform=`translateX(${-(t-14)*40}px)`);
 const R=div(w,"abs","left:540px;top:700px;width:0;height:0;transform:rotate(-12deg)");
 const BH=360,GAP=22,BW=1700,IW=1320,IH=650;
 const bands=[["coach-lane.jpg","50% 45%","SIM · THE RIG"],["kartPan.jpg","48% 55%","KART · FULL SEND"],["fsCarBw.jpg","18% 80%","FORMULA STUDENT"]].map(([s,pos,lab],i)=>{
  const b=div(R,"pn",`left:${-BW/2}px;top:${(i-1)*(BH+GAP)-BH/2}px;width:${BW}px;height:${BH}px`,
   `<img src="assets/${s}" style="position:absolute;left:${(BW-IW)/2}px;top:${(BH-IH)/2}px;width:${IW}px;height:${IH}px;object-fit:cover;object-position:${pos};filter:grayscale(.3) contrast(1.12) brightness(.82) saturate(.85)"/><div class="tint2"></div>`);
  div(b,"cap",`left:${BW/2-430}px;bottom:24px;font-size:18px`,lab);return [b,b.querySelector("img")]});
 const T=title(w,90,1450,120,["SIM TO","TARMAC."],"02 · Motorsport","sim · karts · formula student");
 on(t=>{rise(T.h,t,14.5,.04);T.k.style.opacity=P(t,14.4,14.7);T.s.style.opacity=1;typeOn(T.s,t,15.0);
  bands.forEach(([b,img],i)=>{const st=13.95+i*.18,dir=i%2?1:-1;const q=oE(P(t,st,st+.7)),out=iC(P(t,18.25,18.6+i*.03));
   b.style.transform=`translateX(${(1-q)*dir*2000-out*dir*2200+Math.sin(t*.7+i)*8}px)`;
   img.style.transform=`rotate(12deg) translateX(${(t-st)*-8*dir}px) scale(${lerp(1.08,1.02,oC(P(t,st,st+4)))})`});
  T.w.style.opacity=1-P(t,18.25,18.5)});
 sfx("thock",18.55,.8);}

/* ---------------- S6: BEHIND THE SCENES ---------------- */
{const w=$("#s6w");const bg=div(w,"abs","inset:-80px;background:url(assets/08-dither-gradient-overlay.png) center/cover;opacity:.25");on(t=>bg.style.transform=`scale(${1+(t-18.5)*.02})`);
 const T=title(w,90,150,130,["OFF THE","CLOCK."],"03 · Behind the scenes","coaching · data · the build");
 const C=[["coach-brief.jpg","50% 40%",-4,"THE BRIEF"],["telemetry-c.jpg","50% 50%",3,"THE DATA"],["fs-iterate.jpg","50% 50%",-2,"THE BUILD"],["coach-data.jpg","50% 45%",2,"THE DEBRIEF"]];
 const cards=C.map(([s,pos,r,lab])=>{const p=panel(w,s,140,760,800,720,pos,false);p.o.style.border="2px solid rgba(243,244,246,.5)";div(p.o,"cap","left:28px;bottom:24px",lab);return [p,r]});
 on(t=>{rise(T.h,t,18.75,.035);T.k.style.opacity=P(t,18.65,18.95);T.s.style.opacity=1;typeOn(T.s,t,19.3);
  cards.forEach(([p,r],i)=>{const st=18.95+i*.55;const q=oE(P(t,st,st+.45));const above=cl((t-(st+.55))/.55,0,3);
   p.o.style.opacity=t>=st?1:0;p.o.style.zIndex=i;
   p.o.style.transform=`translateY(${(1-q)*900-above*14}px) rotate(${r*(1-.4*q)+(1-q)*r*3}deg) scale(${lerp(1.15,1,q)-above*.03})`;
   p.img.style.filter=`grayscale(.3) contrast(1.12) brightness(${.85-above*.15})`;
   p.img.style.transform=`scale(${lerp(1.12,1.02,oC(P(t,st,st+4)))})`})});
 sfx("thock",22.55,.8);}
SH=-3.15;

/* ---------------- S7: what's coming to the feed ---------------- */
{const w=$("#s7w");const bg=div(w,"abs","inset:-80px;background:url(assets/02-pinstripe-overlay.png) center/cover;opacity:.18");on(t=>bg.style.transform=`translateX(${(t-24)*-16}px)`);
 const T=title(w,90,150,130,["ON THE","FEED."],"What's coming","new every week");
 const IT=["SIM RACING HOTLAPS","RACECRAFT TIPS","MOTORSPORT LIFESTYLE","RIG & SETUP TOURS","BEHIND THE SCENES"];
 const rows=IT.map((x,i)=>{const r=div(w,"abs",`left:90px;top:${660+i*170}px;width:900px;height:150px`);
  const n=div(r,"abs m",`left:0;top:44px;font-size:22px;color:${SKY}`,`0${i+1}`);
  const tx=div(r,"abs h",`left:96px;top:28px;font-size:62px`,`<span class="line" data-split>${x}</span>`);split(tx);
  const ln=div(r,"abs",`left:0;bottom:0;height:1px;width:0;background:rgba(243,244,246,.25)`);
  const hl=div(r,"abs",`left:-24px;top:16px;width:6px;height:96px;background:${BLUE};opacity:0`);
  return {r,n,tx,ln,hl}});
 const R0=25.05,DR=.42;
 rows.forEach((_,i)=>sfx("thock",R0+i*DR,.45));
 on(t=>{rise(T.h,t,24.55,.04);T.k.style.opacity=P(t,24.5,24.8);T.s.style.opacity=1;typeOn(T.s,t,25.0);
  rows.forEach(({r,n,tx,ln,hl},i)=>{const st=R0+i*DR;
   n.style.opacity=P(t,st,st+.2);rise(tx,t,st,.018,.45);ln.style.width=900*ioC(P(t,st,st+.6))+"px";
   const cur=t>=st&&t<st+DR+.05||(i===4&&t>=st);hl.style.opacity=cur?1:0;
   tx.style.color=t<st+DR||i===4?ICE:STEEL;
   const o=iC(P(t,27.75+i*.04,28.05+i*.04));r.style.transform=`translateX(${-o*1200}px)`});
  T.w.style.opacity=1-P(t,27.8,28.05)});
 sfx("thock",28.1,.8);}

/* ---------------- S8: lockup + sign-off ---------------- */
SH=-1.63;
{const w=$("#s8w");const [vx,vy,vw,vh]=LOGO.lvb.split(" ").map(Number);const LW2=900,sc=LW2/vw,h=vh*sc;
 const lk=div(w,"abs",`left:${(1080-LW2)/2}px;top:700px;width:${LW2}px;height:${h}px`,`<svg viewBox="${LOGO.lvb}" width="${LW2}" height="${h}">${LOGO.lockup}</svg>`);
 let cq="";const sq=20,rows=4;for(let c=-3;c<60;c++)for(let r=0;r<rows;r++){if((c+r)%2)continue;const x=c*sq,y=r*sq,d=Math.min(1,Math.abs(x+sq/2-540)/540),op=Math.pow(1-d,1.6)*(1-r/rows*.75);if(op<.02)continue;const dy=(rows-r)*sq;
  cq+=`<polygon points="${x+dy*K},${y} ${x+sq+dy*K},${y} ${x+sq+(dy-sq)*K},${y+sq} ${x+(dy-sq)*K},${y+sq}" fill="#F3F4F6" opacity="${(op*.55).toFixed(2)}"/>`}
 const band=div(w,"abs","left:0;top:1250px;width:1080px;height:80px",`<svg width="1080" height="80">${cq}</svg>`);
 const hdl=div(w,"abs m","left:0;right:0;top:1400px;text-align:center;font-size:30px;color:#F3F4F6","");
 const tag=div(w,"abs m","left:0;right:0;top:1460px;text-align:center;font-size:18px;color:#8C93A3","SIM · TRACK · PADDOCK");
 radio(w,90,1580,"AKKI","Copy. See you on track.",28.45,32.6);
 sfx("hit",27.08,1);
 for(let i=0;i<13;i++)sfx("type",28.0+i*.045,.35);
 on(t=>{const q=oE(P(t,27.05,27.7));lk.style.clipPath=`inset(0 ${(1-q)*100}% 0 0)`;lk.style.transform=`scale(${lerp(1.08,1,oC(P(t,27.05,29.8)))})`;
  band.style.opacity=P(t,27.6,28.1);band.style.transform=`translateX(${(1-oE(P(t,27.6,28.3)))*-80}px)`;
  const s="@akki_meister";hdl.textContent=s.slice(0,Math.floor(cl((t-28.0)/.045,0,s.length)));tag.style.opacity=P(t,28.4,28.7)});}
SH=0;

/* ---------------- render ---------------- */
const SC=[["#s1",0,4.55],["#s2",4.3,7.9],["#s4",7.85,12.65],["#s5",12.6,17.35],["#s6",17.25,21.3],["#s7",21.25,25.45],["#s8",25.4,END+.1]];

window.render=function(t){
  SC.forEach(([s,a,b])=>$(s).style.display=t>=a&&t<b?"block":"none");
  UP.forEach(f=>f(t));
  const gk=Math.floor(t*12);$("#grain").style.transform=`translate(${(gk*37)%60-30}px,${(gk*53)%60-30}px)`;
  $("#glow").style.opacity=.6+.4*Math.sin(t*1.3);
  $("#stage").style.filter=`brightness(${P(t,0,.4)*(1-P(t,END-.45,END))})`;
};
window.END=END;
window.ready=(async()=>{await Promise.all(["600 100px ClashD","600 20px Clash","500 20px JBM"].map(f=>document.fonts.load(f)));await document.fonts.ready;
 await Promise.all([...document.images].map(i=>i.complete?0:new Promise(r=>i.onload=i.onerror=r)));window.render(0);return true})();
</script></body></html>
