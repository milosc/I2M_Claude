import{j as t}from"./jsx-runtime-CDt2p4po.js";import{a as T}from"./index-B-lxVbXh.js";import{at as y,az as O,bb as It,b as c,c as oe,H as tt,d as bt,a as g,aq as it,V as j,ad as Lt,h as U,av as re}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{r as Bt}from"./index-GiUgBvb1.js";import{$ as Mt}from"./GridLayout-Bc3SIaYk.js";import{c as vt,d as ot,b as R,a as P,$ as rt}from"./ListLayout-8Q9Kcx4Y.js";import{u as W}from"./useDragAndDrop--5mYXGU7.js";import{a as l,L as st}from"./utils-N1pTmi3h.js";import{s as h}from"./index.module-B9nxguEg.js";/* empty css               */import"./v4-CtRu48qb.js";import"./index-C8NrMXaH.js";import"./useDrag-D4nPEkp-.js";class zt extends ot{copy(){let i=super.copy();return i.column=this.column,i.index=this.index,i}constructor(...i){super(...i),this.column=0,this.index=0}}const u={minItemSize:new y(200,200),maxItemSize:new y(1/0,1/0),minSpace:new y(18,18),maxSpace:1/0,maxColumns:1/0,dropIndicatorThickness:2};class jt extends vt{shouldInvalidateLayoutOptions(i,o){return i.maxColumns!==o.maxColumns||i.dropIndicatorThickness!==o.dropIndicatorThickness||!(i.minItemSize||u.minItemSize).equals(o.minItemSize||u.minItemSize)||!(i.maxItemSize||u.maxItemSize).equals(o.maxItemSize||u.maxItemSize)||!(i.minSpace||u.minSpace).equals(o.minSpace||u.minSpace)||i.maxHorizontalSpace!==o.maxHorizontalSpace}update(i){var o;let{minItemSize:e=u.minItemSize,maxItemSize:a=u.maxItemSize,minSpace:n=u.minSpace,maxHorizontalSpace:r=u.maxSpace,maxColumns:d=u.maxColumns,dropIndicatorThickness:x=u.dropIndicatorThickness}=i.layoutOptions||{};this.dropIndicatorThickness=x;let f=this.virtualizer.visibleRect.width,I=Math.min(a.width,f),se=Number.isFinite(a.height)?a.height:Math.floor(e.height/e.width*I),dt=Math.floor(f/(e.width+n.width)),b=Math.max(1,Math.min(d,dt)),ct=f-n.width*Math.max(0,b),L=Math.floor(ct/b);L=Math.max(e.width,Math.min(I,L));let mt=(L-e.width)/Math.max(1,I-e.width),Q=e.height+Math.floor((se-e.height)*mt);Q=Math.max(e.height,Math.min(se,Q));let F=Math.min(Math.max(r,n.width),Math.floor((f-b*L)/(b+1)));this.margin=Math.floor((f-b*L-F*(b+1))/2);let B=Array(b).fill(n.height),ee=new Map,ae=0,ne=(p,v)=>{let m=this.layoutInfos.get(p),w=Q,le=!0;m&&(w=m.rect.height/m.rect.width*L,le=i.sizeChanged||m.estimatedSize||m.content!==v);let ie=b===this.numColumns&&m&&m.index===ae&&m.rect.y<this.virtualizer.visibleRect.maxY?m.column:void 0,Y=ie??B.reduce((de,yt,ft)=>yt<B[de]?ft:de,0),ut=F+Y*(L+F)+this.margin,xt=B[Y],gt=new O(ut,xt,L,w),z=new zt(v.type,p,gt);z.estimatedSize=le,z.allowOverflow=!0,z.content=v,z.column=Y,z.index=ae++,ee.set(p,z),B[Y]+=z.rect.height+n.height},M=this.virtualizer.collection,ht=0;for(let p of M)if(p.type==="skeleton"){let v=[...B];for(;!B.every((m,w)=>m!==v[w])||Math.min(...B)<this.virtualizer.visibleRect.height;){var te;let m=`${p.key}-${ht++}`,w=((te=this.layoutInfos.get(m))===null||te===void 0?void 0:te.content)||{...p};ne(m,w)}break}else p.type!=="loader"&&ne(p.key,p);let A=M.getItem(M.getLastKey());if((A==null?void 0:A.type)==="loader"){let p=new O(F,B[0],L,0),v=new ot("loader",A.key,p);ee.set(A.key,v)}let pt=(M==null?void 0:M.size)===0&&((o=M.getItem(M.getFirstKey()))===null||o===void 0?void 0:o.type)!=="skeleton"?0:Math.max(...B);this.contentSize=new y(this.virtualizer.visibleRect.width,pt),this.layoutInfos=ee,this.numColumns=b}getLayoutInfo(i){return this.layoutInfos.get(i)}getContentSize(){return this.contentSize}getVisibleLayoutInfos(i){let o=[];for(let e of this.layoutInfos.values())(e.rect.intersects(i)||this.virtualizer.isPersistedKey(e.key)||e.type==="loader")&&o.push(e);return o}updateItemSize(i,o){let e=this.layoutInfos.get(i);if(!o||!e)return!1;if(o.height!==e.rect.height){let a=e.copy();return a.rect.height=o.height,a.estimatedSize=!1,this.layoutInfos.set(i,a),!0}return!1}getKeyRightOf(i){let o=this.getLayoutInfo(i);if(!o)return null;let e=new O(o.rect.maxX,o.rect.y,this.virtualizer.visibleRect.maxX-o.rect.maxX,o.rect.height),a=this.getVisibleLayoutInfos(e),n=null,r=1/0;for(let d of a){if(d.key===i)continue;let x=d.rect.x-e.x,f=Math.min(d.rect.maxY,e.maxY)-Math.max(d.rect.y,e.y),I=x-f;I<r&&(r=I,n=d.key)}return n}getKeyLeftOf(i){let o=this.getLayoutInfo(i);if(!o)return null;let e=new O(0,o.rect.y,o.rect.x,o.rect.height),a=this.getVisibleLayoutInfos(e),n=null,r=1/0;for(let d of a){if(d.key===i)continue;let x=e.maxX-d.rect.maxX,f=Math.min(d.rect.maxY,e.maxY)-Math.max(d.rect.y,e.y),I=x-f;I<r&&(r=I,n=d.key)}return n}getKeyRange(i,o){let e=this.getLayoutInfo(i),a=this.getLayoutInfo(o);if(!e||!a)return[];let n=e.rect.union(a.rect),r=[];for(let d of this.layoutInfos.values())n.intersection(d.rect).area>d.rect.area/2&&r.push(d.key);return r}getDropTargetFromPoint(i,o){if(this.layoutInfos.size===0)return{type:"root"};i+=this.virtualizer.visibleRect.x,o+=this.virtualizer.visibleRect.y;let e=this.virtualizer.keyAtPoint(new It(i,o));return e==null?{type:"root"}:{type:"item",key:e,dropPosition:"on"}}constructor(...i){super(...i),this.contentSize=new y,this.layoutInfos=new Map,this.numColumns=0,this.dropIndicatorThickness=2,this.margin=0}}const qt={title:"React Aria Components/ListBox",component:c,excludeStories:["MyListBoxLoaderIndicator"]},S=s=>t.jsxs(c,{className:h.menu,...s,"aria-label":"test listbox",children:[t.jsx(l,{children:"Foo"}),t.jsx(l,{children:"Bar"}),t.jsx(l,{children:"Baz"}),t.jsx(l,{href:"http://google.com",children:"Google"})]});S.story={args:{selectionMode:"none",selectionBehavior:"toggle",shouldFocusOnHover:!1,escapeKeyBehavior:"clearSelection"},argTypes:{selectionMode:{control:"radio",options:["none","single","multiple"]},selectionBehavior:{control:"radio",options:["toggle","replace"]},escapeKeyBehavior:{control:"radio",options:["clearSelection","none"]}},parameters:{description:{data:"Hover styles should have higher specificity than focus style for testing purposes. Hover style should not be applied on keyboard focus even if shouldFocusOnHover is true"}}};const $=()=>t.jsxs(c,{className:h.menu,selectionMode:"multiple",selectionBehavior:"replace","aria-label":"test listbox with section",children:[t.jsxs(oe,{className:h.group,children:[t.jsx(tt,{style:{fontSize:"1.2em"},children:"Section 1"}),t.jsx(l,{children:"Foo"}),t.jsx(l,{children:"Bar"}),t.jsx(l,{children:"Baz"})]}),t.jsx(bt,{style:{borderTop:"1px solid gray",margin:"2px 5px"}}),t.jsxs(oe,{className:h.group,"aria-label":"Section 2",children:[t.jsx(l,{children:"Foo"}),t.jsx(l,{children:"Bar"}),t.jsx(l,{children:"Baz"})]})]}),C=()=>t.jsxs(c,{className:h.menu,selectionMode:"multiple",selectionBehavior:"replace","aria-label":"listbox complex",children:[t.jsxs(l,{children:[t.jsx(g,{slot:"label",children:"Item 1"}),t.jsx(g,{slot:"description",children:"Description"})]}),t.jsxs(l,{children:[t.jsx(g,{slot:"label",children:"Item 2"}),t.jsx(g,{slot:"description",children:"Description"})]}),t.jsxs(l,{children:[t.jsx(g,{slot:"label",children:"Item 3"}),t.jsx(g,{slot:"description",children:"Description"})]})]});let at=[{id:1,image:"https://images.unsplash.com/photo-1593958812614-2db6a598c71c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8ZGlzY298ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=900&q=60",title:"Euphoric Echoes",artist:"Luna Solstice"},{id:2,image:"https://images.unsplash.com/photo-1601042879364-f3947d3f9c16?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmVvbnxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=900&q=60",title:"Neon Dreamscape",artist:"Electra Skyline"},{id:3,image:"https://images.unsplash.com/photo-1528722828814-77b9b83aafb2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHNwYWNlfGVufDB8fDB8fHww&auto=format&fit=crop&w=900&q=60",title:"Cosmic Serenade",artist:"Orion's Symphony"},{id:4,image:"https://images.unsplash.com/photo-1511379938547-c1f69419868d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bXVzaWN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=900&q=60",title:"Melancholy Melodies",artist:"Violet Mistral"},{id:5,image:"https://images.unsplash.com/photo-1608433319511-dfe8ea4cbd3c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGJlYXR8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=900&q=60",title:"Rhythmic Illusions",artist:"Mirage Beats"}];const k=s=>{let i=R({initialItems:at}),{dragAndDropHooks:o}=W({getItems:(e,a)=>a.map(n=>({"text/plain":n.title??""})),onReorder(e){e.target.dropPosition==="before"?i.moveBefore(e.target.key,e.keys):e.target.dropPosition==="after"&&i.moveAfter(e.target.key,e.keys)}});return t.jsx(c,{...s,"aria-label":"Albums",items:i.items,selectionMode:"multiple",dragAndDropHooks:o,children:e=>t.jsxs(it,{children:[t.jsx("img",{src:e.image,alt:""}),t.jsx(g,{slot:"label",children:e.title}),t.jsx(g,{slot:"description",children:e.artist})]})})};k.story={args:{layout:"stack",orientation:"horizontal"},argTypes:{layout:{control:"radio",options:["stack","grid"]},orientation:{control:"radio",options:["horizontal","vertical"]}}};function wt({mode:s,offsetX:i,offsetY:o,...e}){let a=R({initialItems:at}),{dragAndDropHooks:n}=W({getItems:r=>[...r].map(d=>{var x;return{"text/plain":((x=a.getItem(d))==null?void 0:x.title)??""}}),onReorder(r){r.target.dropPosition==="before"?a.moveBefore(r.target.key,r.keys):r.target.dropPosition==="after"&&a.moveAfter(r.target.key,r.keys)},renderDragPreview(r){let d=t.jsxs("div",{style:{display:"flex",alignItems:"center",padding:4,background:"white",border:"1px solid gray"},children:[t.jsx(g,{children:r[0]["text/plain"]}),r.length>1&&t.jsxs("span",{style:{marginLeft:4,fontSize:12},children:["+",r.length-1]})]});return s==="custom"?{element:d,x:i,y:o}:d}});return t.jsx(c,{...e,"aria-label":"Albums with preview offset",items:a.items,selectionMode:"multiple",dragAndDropHooks:n,children:r=>t.jsxs(it,{children:[t.jsx("img",{src:r.image,alt:""}),t.jsx(g,{slot:"label",children:r.title}),t.jsx(g,{slot:"description",children:r.artist})]})})}const G={render(s){return t.jsx(wt,{...s})},args:{layout:"stack",orientation:"horizontal",mode:"default",offsetX:20,offsetY:20},argTypes:{layout:{control:"radio",options:["stack","grid"]},orientation:{control:"radio",options:["horizontal","vertical"]},mode:{control:"select",options:["default","custom"]},offsetX:{control:"number"},offsetY:{control:"number"}}},V=()=>t.jsxs(c,{className:h.menu,"aria-label":"test listbox",onAction:T("onAction"),children:[t.jsx(l,{onHoverStart:T("onHoverStart"),onHoverChange:T("onHoverChange"),onHoverEnd:T("onHoverEnd"),children:"Hover"}),t.jsx(l,{children:"Bar"}),t.jsx(l,{children:"Baz"}),t.jsx(l,{href:"http://google.com",children:"Google"})]}),H=s=>t.jsxs(c,{...s,className:h.menu,"aria-label":"test listbox",style:{width:300,height:300,display:"grid",gridTemplate:"repeat(3, 1fr) / repeat(3, 1fr)",gridAutoFlow:s.orientation==="vertical"?"row":"column"},children:[t.jsx(l,{style:{display:"flex",alignItems:"center",justifyContent:"center"},children:"1,1"}),t.jsx(l,{style:{display:"flex",alignItems:"center",justifyContent:"center"},children:"1,2"}),t.jsx(l,{style:{display:"flex",alignItems:"center",justifyContent:"center"},children:"1,3"}),t.jsx(l,{style:{display:"flex",alignItems:"center",justifyContent:"center"},children:"2,1"}),t.jsx(l,{style:{display:"flex",alignItems:"center",justifyContent:"center"},children:"2,2"}),t.jsx(l,{style:{display:"flex",alignItems:"center",justifyContent:"center"},children:"2,3"}),t.jsx(l,{style:{display:"flex",alignItems:"center",justifyContent:"center"},children:"3,1"}),t.jsx(l,{style:{display:"flex",alignItems:"center",justifyContent:"center"},children:"3,2"}),t.jsx(l,{style:{display:"flex",alignItems:"center",justifyContent:"center"},children:"3,3"})]});H.story={args:{layout:"grid",orientation:"vertical"},argTypes:{orientation:{control:{type:"radio",options:["vertical","horizontal"]}}}};function St(s,i){const o="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",e=Math.floor(Math.random()*(i-s+1))+s;let a="";for(let n=0;n<e;n++)a+=o.charAt(Math.floor(Math.random()*o.length));return a}function kt({variableHeight:s,isLoading:i}){let o=[];for(let e=0;e<10;e++){let a=[];for(let n=0;n<100;n++){const r=e*5+n+10;a.push({id:`item_${e}_${n}`,name:`Section ${e}, Item ${n}${s?" "+St(r,r):""}`})}o.push({id:`section_${e}`,name:`Section ${e}`,children:a})}return t.jsx(j,{layout:new P({estimatedRowHeight:25,estimatedHeadingHeight:26,loaderHeight:30}),children:t.jsxs(c,{className:h.menu,style:{height:400},"aria-label":"virtualized listbox",children:[t.jsx(U,{items:o,children:e=>t.jsxs(oe,{className:h.group,children:[t.jsx(tt,{style:{fontSize:"1.2em"},children:e.name}),t.jsx(U,{items:e.children,children:a=>t.jsx(l,{children:a.name})})]})}),t.jsx(_,{orientation:"vertical",isLoading:i})]})})}const X={render:s=>t.jsx(kt,{...s}),args:{variableHeight:!1,isLoading:!1}};let K={render:()=>t.jsx(j,{layout:P,layoutOptions:{rowHeight:25,estimatedHeadingHeight:26},children:t.jsx(c,{className:h.menu,style:{height:400},"aria-label":"virtualized listbox",renderEmptyState:()=>"Empty",children:t.jsx(_,{})})})},N=()=>{let s=[];for(let e=0;e<1e4;e++)s.push({id:e,name:`Item ${e}`});let i=R({initialItems:s}),{dragAndDropHooks:o}=W({getItems:e=>[...e].map(a=>{var n;return{"text/plain":((n=i.getItem(a))==null?void 0:n.name)??""}}),onReorder(e){e.target.dropPosition==="before"?i.moveBefore(e.target.key,e.keys):e.target.dropPosition==="after"&&i.moveAfter(e.target.key,e.keys)},renderDropIndicator(e){return t.jsx(re,{target:e,style:({isDropTarget:a})=>({width:"100%",height:"100%",background:a?"blue":"transparent"})})}});return t.jsx("div",{style:{height:400,width:400,resize:"both",padding:40,overflow:"hidden"},children:t.jsx(j,{layout:P,layoutOptions:{rowHeight:25,gap:8},children:t.jsx(c,{className:h.menu,selectionMode:"multiple",selectionBehavior:"replace",style:{width:"100%",height:"100%"},"aria-label":"virtualized listbox",items:i.items,dragAndDropHooks:o,children:e=>t.jsx(l,{children:e.name})})})})};function Ht({minSize:s=80,maxSize:i=100,preserveAspectRatio:o=!1}){let e=[];for(let r=0;r<1e4;r++)e.push({id:r,name:`Item ${r}`});let a=R({initialItems:e}),{dragAndDropHooks:n}=W({getItems:r=>[...r].map(d=>{var x;return{"text/plain":((x=a.getItem(d))==null?void 0:x.name)??""}}),onReorder(r){r.target.dropPosition==="before"?a.moveBefore(r.target.key,r.keys):r.target.dropPosition==="after"&&a.moveAfter(r.target.key,r.keys)},renderDropIndicator(r){return t.jsx(re,{target:r,style:({isDropTarget:d})=>({width:"100%",height:"100%",background:d?"blue":"transparent"})})}});return t.jsx("div",{style:{height:400,width:400,resize:"both",padding:40,overflow:"hidden"},children:t.jsx(j,{layout:Mt,layoutOptions:{minItemSize:new y(s,s),maxItemSize:new y(i,i),preserveAspectRatio:o},children:t.jsx(c,{className:h.menu,selectionMode:"multiple",selectionBehavior:"replace",layout:"grid",style:{width:"100%",height:"100%"},"aria-label":"virtualized listbox",items:a.items,dragAndDropHooks:n,children:r=>t.jsx(l,{style:{height:"100%",border:"1px solid",boxSizing:"border-box"},children:r.name})})})})}const q={render:s=>t.jsx(Ht,{...s}),args:{minSize:80,maxSize:100,preserveAspectRatio:!1}};let Dt="Lorem ipsum dolor sit amet, consectetur adipiscing elit.".split(" "),nt=[];for(let s=0;s<1e3;s++){let i=Math.max(2,Math.floor(Math.random()*25)),o=Dt.slice(0,i).join(" ");nt.push({id:s,name:o})}function At({minSize:s=40,maxSize:i=65,maxColumns:o=void 0,minSpace:e=void 0,maxSpace:a=void 0}){let[n]=Bt.useState(nt);return t.jsx("div",{style:{height:400,width:400,resize:"both",padding:40,overflow:"hidden"},children:t.jsx(j,{layout:jt,layoutOptions:{minItemSize:new y(s,40),maxItemSize:new y(i,65),maxColumns:o,minSpace:new y(e,18),maxHorizontalSpace:a},children:t.jsx(c,{className:h.menu,selectionMode:"multiple",selectionBehavior:"replace",layout:"grid",style:{width:"100%",height:"100%"},"aria-label":"virtualized listbox",items:n,children:r=>t.jsx(l,{style:{height:"100%",border:"1px solid",boxSizing:"border-box"},children:r.name})})})})}const Z={render:s=>t.jsx(At,{...s}),args:{minSize:40,maxSize:65,maxColumns:void 0,minSpace:void 0,maxSpace:void 0},argTypes:{minSize:{control:"number",description:"The minimum width of each item in the grid list",defaultValue:40},maxSize:{control:"number",description:"Maximum width of each item in the grid list.",defaultValue:65},maxColumns:{control:"number",description:"Maximum number of columns in the grid list.",defaultValue:void 0},minSpace:{control:"number",description:"Minimum horizontal space between grid items.",defaultValue:void 0},maxSpace:{control:"number",description:"Maximum horizontal space between grid items.",defaultValue:void 0}}};let lt=({isLoading:s})=>t.jsx("div",{style:{height:30,width:"100%"},children:s?t.jsx(st,{style:{height:20,width:20,transform:"translate(-50%, -50%)"}}):"No results"});const _=s=>{let{orientation:i,...o}=s;return t.jsx(Lt,{style:{height:i==="horizontal"?100:30,width:i==="horizontal"?30:"100%",flexShrink:0,display:"flex",alignItems:"center",justifyContent:"center"},...o,children:t.jsx(st,{style:{height:20,width:20,position:"unset"}})})};function Tt(s){let i=rt({async load({signal:o,cursor:e,filterText:a}){e&&(e=e.replace(/^http:\/\//i,"https://")),await new Promise(d=>setTimeout(d,s.delay));let r=await(await fetch(e||`https://swapi.py4e.com/api/people/?search=${a}`,{signal:o})).json();return{items:r.results,cursor:r.next}}});return t.jsxs(c,{...s,style:{height:s.orientation==="horizontal"?"fit-content":400,width:s.orientation==="horizontal"?400:200,overflow:"auto"},"aria-label":"async listbox",renderEmptyState:()=>lt({isLoading:i.isLoading}),children:[t.jsx(U,{items:i.items,children:o=>t.jsx(l,{style:{minHeight:s.orientation==="horizontal"?100:50,minWidth:s.orientation==="horizontal"?50:200,backgroundColor:"lightgrey",border:"1px solid black",boxSizing:"border-box"},id:o.name,children:o.name})}),t.jsx(_,{orientation:s.orientation,isLoading:i.loadingState==="loadingMore",onLoadMore:i.loadMore})]})}const J={render:s=>t.jsx(Tt,{...s}),args:{orientation:"horizontal",delay:50},argTypes:{orientation:{control:"radio",options:["horizontal","vertical"]}}},D=s=>{let i=rt({async load({signal:o,cursor:e,filterText:a}){e&&(e=e.replace(/^http:\/\//i,"https://")),await new Promise(d=>setTimeout(d,s.delay));let r=await(await fetch(e||`https://swapi.py4e.com/api/people/?search=${a}`,{signal:o})).json();return{items:r.results,cursor:r.next}}});return t.jsx(j,{layout:P,layoutOptions:{rowHeight:50,padding:4,loaderHeight:30},children:t.jsxs(c,{...s,style:{height:400,width:100,border:"1px solid gray",background:"lightgray",overflow:"auto",padding:"unset",display:"flex"},"aria-label":"async virtualized listbox",renderEmptyState:()=>lt({isLoading:i.isLoading}),children:[t.jsx(U,{items:i.items,children:o=>t.jsx(l,{style:{backgroundColor:"lightgrey",border:"1px solid black",boxSizing:"border-box",height:"100%",width:"100%"},id:o.name,children:o.name})}),t.jsx(_,{isLoading:i.loadingState==="loadingMore",onLoadMore:i.loadMore})]})})};D.story={args:{delay:50}};let E=()=>{let s=[];for(let e=0;e<100;e++)s.push({id:e,name:`Item ${e}`});let i=R({initialItems:s}),{dragAndDropHooks:o}=W({getItems:e=>[...e].map(a=>{var n;return{"text/plain":((n=i.getItem(a))==null?void 0:n.name)??""}}),onReorder(e){e.target.dropPosition==="before"?i.moveBefore(e.target.key,e.keys):e.target.dropPosition==="after"&&i.moveAfter(e.target.key,e.keys)},renderDropIndicator(e){return t.jsx(re,{target:e,style:({isDropTarget:a})=>({width:"100%",height:2,background:a?"blue":"gray",margin:"2px 0"})})}});return t.jsxs("div",{style:{display:"flex",flexDirection:"column",gap:20,alignItems:"center"},children:[t.jsxs("div",{style:{padding:20,background:"#f0f0f0",borderRadius:8,maxWidth:600},children:[t.jsx("h3",{style:{margin:"0 0 10px 0"},children:"Instructions:"}),t.jsxs("ul",{style:{margin:0,paddingLeft:20},children:[t.jsxs("li",{children:[t.jsx("strong",{children:"Enter:"})," Triggers onAction"]}),t.jsxs("li",{children:[t.jsx("strong",{children:"Alt+Enter:"})," Starts drag mode"]}),t.jsxs("li",{children:[t.jsx("strong",{children:"Space:"})," Toggles selection"]})]})]}),t.jsx("div",{style:{height:400,width:300,resize:"both",padding:20,overflow:"hidden",border:"2px solid #ccc",borderRadius:8},children:t.jsx(j,{layout:P,layoutOptions:{rowHeight:25,gap:4},children:t.jsx(c,{className:h.menu,selectionMode:"multiple",style:{width:"100%",height:"100%"},"aria-label":"Virtualized listbox with drag and drop and onAction",items:i.items,dragAndDropHooks:o,onAction:T("onAction"),children:e=>t.jsx(l,{children:e.name})})})})]})};S.__docgenInfo={description:"",methods:[],displayName:"ListBoxExample"};$.__docgenInfo={description:"",methods:[],displayName:"ListBoxSections"};C.__docgenInfo={description:"",methods:[],displayName:"ListBoxComplex"};k.__docgenInfo={description:"",methods:[],displayName:"ListBoxDnd"};V.__docgenInfo={description:"",methods:[],displayName:"ListBoxHover"};H.__docgenInfo={description:"",methods:[],displayName:"ListBoxGrid"};N.__docgenInfo={description:"",methods:[],displayName:"VirtualizedListBoxDnd"};_.__docgenInfo={description:"",methods:[],displayName:"MyListBoxLoaderIndicator"};D.__docgenInfo={description:"",methods:[],displayName:"AsyncListBoxVirtualized"};E.__docgenInfo={description:"",methods:[],displayName:"VirtualizedListBoxDndOnAction"};var ce,me,he;S.parameters={...S.parameters,docs:{...(ce=S.parameters)==null?void 0:ce.docs,source:{originalSource:`args => <ListBox className={styles.menu} {...args} aria-label="test listbox">
    <MyListBoxItem>Foo</MyListBoxItem>
    <MyListBoxItem>Bar</MyListBoxItem>
    <MyListBoxItem>Baz</MyListBoxItem>
    <MyListBoxItem href="http://google.com">Google</MyListBoxItem>
  </ListBox>`,...(he=(me=S.parameters)==null?void 0:me.docs)==null?void 0:he.source}}};var pe,ue,xe;$.parameters={...$.parameters,docs:{...(pe=$.parameters)==null?void 0:pe.docs,source:{originalSource:`() => <ListBox className={styles.menu} selectionMode="multiple" selectionBehavior="replace" aria-label="test listbox with section">
    <ListBoxSection className={styles.group}>
      <Header style={{
      fontSize: '1.2em'
    }}>Section 1</Header>
      <MyListBoxItem>Foo</MyListBoxItem>
      <MyListBoxItem>Bar</MyListBoxItem>
      <MyListBoxItem>Baz</MyListBoxItem>
    </ListBoxSection>
    <Separator style={{
    borderTop: '1px solid gray',
    margin: '2px 5px'
  }} />
    <ListBoxSection className={styles.group} aria-label="Section 2">
      <MyListBoxItem>Foo</MyListBoxItem>
      <MyListBoxItem>Bar</MyListBoxItem>
      <MyListBoxItem>Baz</MyListBoxItem>
    </ListBoxSection>
  </ListBox>`,...(xe=(ue=$.parameters)==null?void 0:ue.docs)==null?void 0:xe.source}}};var ge,ye,fe;C.parameters={...C.parameters,docs:{...(ge=C.parameters)==null?void 0:ge.docs,source:{originalSource:`() => <ListBox className={styles.menu} selectionMode="multiple" selectionBehavior="replace" aria-label="listbox complex">
    <MyListBoxItem>
      <Text slot="label">Item 1</Text>
      <Text slot="description">Description</Text>
    </MyListBoxItem>
    <MyListBoxItem>
      <Text slot="label">Item 2</Text>
      <Text slot="description">Description</Text>
    </MyListBoxItem>
    <MyListBoxItem>
      <Text slot="label">Item 3</Text>
      <Text slot="description">Description</Text>
    </MyListBoxItem>
  </ListBox>`,...(fe=(ye=C.parameters)==null?void 0:ye.docs)==null?void 0:fe.source}}};var Ie,be,Le;k.parameters={...k.parameters,docs:{...(Ie=k.parameters)==null?void 0:Ie.docs,source:{originalSource:`props => {
  let list = useListData({
    initialItems: albums
  });
  let {
    dragAndDropHooks
  } = useDragAndDrop<Album>({
    getItems: (keys, items) => items.map(item => ({
      'text/plain': item.title ?? ''
    })),
    onReorder(e) {
      if (e.target.dropPosition === 'before') {
        list.moveBefore(e.target.key, e.keys);
      } else if (e.target.dropPosition === 'after') {
        list.moveAfter(e.target.key, e.keys);
      }
    }
  });
  return <ListBox {...props} aria-label="Albums" items={list.items} selectionMode="multiple" dragAndDropHooks={dragAndDropHooks}>
      {item => <ListBoxItem>
          <img src={item.image} alt="" />
          <Text slot="label">{item.title}</Text>
          <Text slot="description">{item.artist}</Text>
        </ListBoxItem>}
    </ListBox>;
}`,...(Le=(be=k.parameters)==null?void 0:be.docs)==null?void 0:Le.source}}};var Be,Me,ve;G.parameters={...G.parameters,docs:{...(Be=G.parameters)==null?void 0:Be.docs,source:{originalSource:`{
  render(args) {
    return <ListBoxDndWithPreview {...args} />;
  },
  args: {
    layout: 'stack',
    orientation: 'horizontal',
    mode: 'default',
    offsetX: 20,
    offsetY: 20
  },
  argTypes: {
    layout: {
      control: 'radio',
      options: ['stack', 'grid']
    },
    orientation: {
      control: 'radio',
      options: ['horizontal', 'vertical']
    },
    mode: {
      control: 'select',
      options: ['default', 'custom']
    },
    offsetX: {
      control: 'number'
    },
    offsetY: {
      control: 'number'
    }
  }
}`,...(ve=(Me=G.parameters)==null?void 0:Me.docs)==null?void 0:ve.source}}};var ze,je,we;V.parameters={...V.parameters,docs:{...(ze=V.parameters)==null?void 0:ze.docs,source:{originalSource:`() => <ListBox className={styles.menu} aria-label="test listbox" onAction={action('onAction')}>
    <MyListBoxItem onHoverStart={action('onHoverStart')} onHoverChange={action('onHoverChange')} onHoverEnd={action('onHoverEnd')}>Hover</MyListBoxItem>
    <MyListBoxItem>Bar</MyListBoxItem>
    <MyListBoxItem>Baz</MyListBoxItem>
    <MyListBoxItem href="http://google.com">Google</MyListBoxItem>
  </ListBox>`,...(we=(je=V.parameters)==null?void 0:je.docs)==null?void 0:we.source}}};var Se,ke,He;H.parameters={...H.parameters,docs:{...(Se=H.parameters)==null?void 0:Se.docs,source:{originalSource:`args => <ListBox {...args} className={styles.menu} aria-label="test listbox" style={{
  width: 300,
  height: 300,
  display: 'grid',
  gridTemplate: 'repeat(3, 1fr) / repeat(3, 1fr)',
  gridAutoFlow: args.orientation === 'vertical' ? 'row' : 'column'
}}>
    <MyListBoxItem style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>1,1</MyListBoxItem>
    <MyListBoxItem style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>1,2</MyListBoxItem>
    <MyListBoxItem style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>1,3</MyListBoxItem>
    <MyListBoxItem style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>2,1</MyListBoxItem>
    <MyListBoxItem style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>2,2</MyListBoxItem>
    <MyListBoxItem style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>2,3</MyListBoxItem>
    <MyListBoxItem style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>3,1</MyListBoxItem>
    <MyListBoxItem style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>3,2</MyListBoxItem>
    <MyListBoxItem style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>3,3</MyListBoxItem>
  </ListBox>`,...(He=(ke=H.parameters)==null?void 0:ke.docs)==null?void 0:He.source}}};var De,Ae,Te;X.parameters={...X.parameters,docs:{...(De=X.parameters)==null?void 0:De.docs,source:{originalSource:`{
  render: args => <VirtualizedListBoxRender {...args} />,
  args: {
    variableHeight: false,
    isLoading: false
  }
}`,...(Te=(Ae=X.parameters)==null?void 0:Ae.docs)==null?void 0:Te.source}}};var $e,Ce,Ve;K.parameters={...K.parameters,docs:{...($e=K.parameters)==null?void 0:$e.docs,source:{originalSource:`{
  render: () => <Virtualizer layout={ListLayout} layoutOptions={{
    rowHeight: 25,
    estimatedHeadingHeight: 26
  }}>
      <ListBox className={styles.menu} style={{
      height: 400
    }} aria-label="virtualized listbox" renderEmptyState={() => 'Empty'}>
        <MyListBoxLoaderIndicator />
      </ListBox>
    </Virtualizer>
}`,...(Ve=(Ce=K.parameters)==null?void 0:Ce.docs)==null?void 0:Ve.source}}};var Ne,Ee,Re;N.parameters={...N.parameters,docs:{...(Ne=N.parameters)==null?void 0:Ne.docs,source:{originalSource:`() => {
  let items: {
    id: number;
    name: string;
  }[] = [];
  for (let i = 0; i < 10000; i++) {
    items.push({
      id: i,
      name: \`Item \${i}\`
    });
  }
  let list = useListData({
    initialItems: items
  });
  let {
    dragAndDropHooks
  } = useDragAndDrop({
    getItems: keys => {
      return [...keys].map(key => ({
        'text/plain': list.getItem(key)?.name ?? ''
      }));
    },
    onReorder(e) {
      if (e.target.dropPosition === 'before') {
        list.moveBefore(e.target.key, e.keys);
      } else if (e.target.dropPosition === 'after') {
        list.moveAfter(e.target.key, e.keys);
      }
    },
    renderDropIndicator(target) {
      return <DropIndicator target={target} style={({
        isDropTarget
      }) => ({
        width: '100%',
        height: '100%',
        background: isDropTarget ? 'blue' : 'transparent'
      })} />;
    }
  });
  return <div style={{
    height: 400,
    width: 400,
    resize: 'both',
    padding: 40,
    overflow: 'hidden'
  }}>
      <Virtualizer layout={ListLayout} layoutOptions={{
      rowHeight: 25,
      gap: 8
    }}>
        <ListBox className={styles.menu} selectionMode="multiple" selectionBehavior="replace" style={{
        width: '100%',
        height: '100%'
      }} aria-label="virtualized listbox" items={list.items} dragAndDropHooks={dragAndDropHooks}>
          {item => <MyListBoxItem>{item.name}</MyListBoxItem>}
        </ListBox>
      </Virtualizer>
    </div>;
}`,...(Re=(Ee=N.parameters)==null?void 0:Ee.docs)==null?void 0:Re.source}}};var Pe,We,_e;q.parameters={...q.parameters,docs:{...(Pe=q.parameters)==null?void 0:Pe.docs,source:{originalSource:`{
  render: args => {
    return <VirtualizedListBoxGridExample {...args} />;
  },
  args: {
    minSize: 80,
    maxSize: 100,
    preserveAspectRatio: false
  }
}`,...(_e=(We=q.parameters)==null?void 0:We.docs)==null?void 0:_e.source}}};var Fe,Ye,Oe;Z.parameters={...Z.parameters,docs:{...(Fe=Z.parameters)==null?void 0:Fe.docs,source:{originalSource:`{
  render: args => {
    return <VirtualizedListBoxWaterfallExample {...args} />;
  },
  args: {
    minSize: 40,
    maxSize: 65,
    maxColumns: undefined,
    minSpace: undefined,
    maxSpace: undefined
  },
  argTypes: {
    minSize: {
      control: 'number',
      description: 'The minimum width of each item in the grid list',
      defaultValue: 40
    },
    maxSize: {
      control: 'number',
      description: 'Maximum width of each item in the grid list.',
      defaultValue: 65
    },
    maxColumns: {
      control: 'number',
      description: 'Maximum number of columns in the grid list.',
      defaultValue: undefined
    },
    minSpace: {
      control: 'number',
      description: 'Minimum horizontal space between grid items.',
      defaultValue: undefined
    },
    maxSpace: {
      control: 'number',
      description: 'Maximum horizontal space between grid items.',
      defaultValue: undefined
    }
  }
}`,...(Oe=(Ye=Z.parameters)==null?void 0:Ye.docs)==null?void 0:Oe.source}}};var Ge,Xe,Ke;J.parameters={...J.parameters,docs:{...(Ge=J.parameters)==null?void 0:Ge.docs,source:{originalSource:`{
  render: args => <AsyncListBoxRender {...args} />,
  args: {
    orientation: 'horizontal',
    delay: 50
  },
  argTypes: {
    orientation: {
      control: 'radio',
      options: ['horizontal', 'vertical']
    }
  }
}`,...(Ke=(Xe=J.parameters)==null?void 0:Xe.docs)==null?void 0:Ke.source}}};var qe,Ze,Je;D.parameters={...D.parameters,docs:{...(qe=D.parameters)==null?void 0:qe.docs,source:{originalSource:`args => {
  let list = useAsyncList<Character>({
    async load({
      signal,
      cursor,
      filterText
    }) {
      if (cursor) {
        cursor = cursor.replace(/^http:\\/\\//i, 'https://');
      }
      await new Promise(resolve => setTimeout(resolve, args.delay));
      let res = await fetch(cursor || \`https://swapi.py4e.com/api/people/?search=\${filterText}\`, {
        signal
      });
      let json = await res.json();
      return {
        items: json.results,
        cursor: json.next
      };
    }
  });
  return <Virtualizer layout={ListLayout} layoutOptions={{
    rowHeight: 50,
    padding: 4,
    loaderHeight: 30
  }}>
      <ListBox {...args} style={{
      height: 400,
      width: 100,
      border: '1px solid gray',
      background: 'lightgray',
      overflow: 'auto',
      padding: 'unset',
      display: 'flex'
    }} aria-label="async virtualized listbox" renderEmptyState={() => renderEmptyState({
      isLoading: list.isLoading
    })}>
        <Collection items={list.items}>
          {(item: Character) => <MyListBoxItem style={{
          backgroundColor: 'lightgrey',
          border: '1px solid black',
          boxSizing: 'border-box',
          height: '100%',
          width: '100%'
        }} id={item.name}>
              {item.name}
            </MyListBoxItem>}
        </Collection>
        <MyListBoxLoaderIndicator isLoading={list.loadingState === 'loadingMore'} onLoadMore={list.loadMore} />
      </ListBox>
    </Virtualizer>;
}`,...(Je=(Ze=D.parameters)==null?void 0:Ze.docs)==null?void 0:Je.source}}};var Ue,Qe,et;E.parameters={...E.parameters,docs:{...(Ue=E.parameters)==null?void 0:Ue.docs,source:{originalSource:`() => {
  let items: {
    id: number;
    name: string;
  }[] = [];
  for (let i = 0; i < 100; i++) {
    items.push({
      id: i,
      name: \`Item \${i}\`
    });
  }
  let list = useListData({
    initialItems: items
  });
  let {
    dragAndDropHooks
  } = useDragAndDrop({
    getItems: keys => {
      return [...keys].map(key => ({
        'text/plain': list.getItem(key)?.name ?? ''
      }));
    },
    onReorder(e) {
      if (e.target.dropPosition === 'before') {
        list.moveBefore(e.target.key, e.keys);
      } else if (e.target.dropPosition === 'after') {
        list.moveAfter(e.target.key, e.keys);
      }
    },
    renderDropIndicator(target) {
      return <DropIndicator target={target} style={({
        isDropTarget
      }) => ({
        width: '100%',
        height: 2,
        background: isDropTarget ? 'blue' : 'gray',
        margin: '2px 0'
      })} />;
    }
  });
  return <div style={{
    display: 'flex',
    flexDirection: 'column',
    gap: 20,
    alignItems: 'center'
  }}>
      <div style={{
      padding: 20,
      background: '#f0f0f0',
      borderRadius: 8,
      maxWidth: 600
    }}>
        <h3 style={{
        margin: '0 0 10px 0'
      }}>Instructions:</h3>
        <ul style={{
        margin: 0,
        paddingLeft: 20
      }}>
          <li><strong>Enter:</strong> Triggers onAction</li>
          <li><strong>Alt+Enter:</strong> Starts drag mode</li>
          <li><strong>Space:</strong> Toggles selection</li>
        </ul>
      </div>
      <div style={{
      height: 400,
      width: 300,
      resize: 'both',
      padding: 20,
      overflow: 'hidden',
      border: '2px solid #ccc',
      borderRadius: 8
    }}>
        <Virtualizer layout={ListLayout} layoutOptions={{
        rowHeight: 25,
        gap: 4
      }}>
          <ListBox className={styles.menu} selectionMode="multiple" style={{
          width: '100%',
          height: '100%'
        }} aria-label="Virtualized listbox with drag and drop and onAction" items={list.items} dragAndDropHooks={dragAndDropHooks} onAction={action('onAction')}>
            {item => <MyListBoxItem>{item.name}</MyListBoxItem>}
          </ListBox>
        </Virtualizer>
      </div>
    </div>;
}`,...(et=(Qe=E.parameters)==null?void 0:Qe.docs)==null?void 0:et.source}}};const Zt=["ListBoxExample","ListBoxSections","ListBoxComplex","ListBoxDnd","ListBoxPreviewOffset","ListBoxHover","ListBoxGrid","VirtualizedListBox","VirtualizedListBoxEmpty","VirtualizedListBoxDnd","VirtualizedListBoxGrid","VirtualizedListBoxWaterfall","MyListBoxLoaderIndicator","AsyncListBox","AsyncListBoxVirtualized","VirtualizedListBoxDndOnAction"];export{J as AsyncListBox,D as AsyncListBoxVirtualized,C as ListBoxComplex,k as ListBoxDnd,S as ListBoxExample,H as ListBoxGrid,V as ListBoxHover,G as ListBoxPreviewOffset,$ as ListBoxSections,_ as MyListBoxLoaderIndicator,X as VirtualizedListBox,N as VirtualizedListBoxDnd,E as VirtualizedListBoxDndOnAction,K as VirtualizedListBoxEmpty,q as VirtualizedListBoxGrid,Z as VirtualizedListBoxWaterfall,Zt as __namedExportsOrder,qt as default};
