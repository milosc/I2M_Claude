import{j as e}from"./jsx-runtime-CDt2p4po.js";import{a as w}from"./index-B-lxVbXh.js";import{A as f,T as L,L as a,I as n,a as r,S as x,M as j,D as ie,B as d,P as v,b as M,c as de,H as oe,d as Mt,e as me,f as Pt,g as Gt,$ as B,V as le,h as he,G as Wt,i as ae,j as ne,k as Nt,l as zt,C as z,m as Ot,R as O,n as m,o as Dt,p as $t,q as Rt,r as Ht,O as Et,s as ue,t as pe,K as ce,u as A,v as _t}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{r as Bt}from"./index-GiUgBvb1.js";import{T as Kt,M as k}from"./Table.stories-CWTeu0Mm.js";import{$ as Ct,a as xe,b as Ut}from"./ListLayout-8Q9Kcx4Y.js";import{M as c,a as b,L as Xt}from"./utils-N1pTmi3h.js";import{MyGridListItem as S}from"./GridList.stories-AtVMXRo9.js";import{MyListBoxLoaderIndicator as qt}from"./ListBox.stories-CEGZgaMS.js";import{MyTag as D}from"./TagGroup.stories-CfHNTBZW.js";import{s as l}from"./index.module-B9nxguEg.js";/* empty css               */import{$ as Jt}from"./useTreeData-56Dai3Mi.js";import"./v4-CtRu48qb.js";import"./index-C8NrMXaH.js";import"./useDragAndDrop--5mYXGU7.js";import"./useDrag-D4nPEkp-.js";import"./GridLayout-Bc3SIaYk.js";const Ls={title:"React Aria Components/Autocomplete",component:f,args:{onAction:w("onAction"),selectionMode:"multiple",escapeKeyBehavior:"clearSelection",disableVirtualFocus:!1},argTypes:{onAction:{table:{disable:!0}},onSelectionChange:{table:{disable:!0}},selectionMode:{control:"radio",options:["none","single","multiple"]},escapeKeyBehavior:{control:"radio",options:["clearSelection","none"]}}};let wt=t=>e.jsxs(j,{className:l.menu,...t,children:[e.jsxs(ue,{className:l.group,"aria-label":"Section 1",children:[e.jsx(c,{children:"Foo"}),e.jsx(c,{children:"Bar"}),e.jsx(c,{children:"Baz"}),e.jsx(c,{href:"http://google.com",children:"Google"}),e.jsxs(pe,{children:[e.jsx(c,{children:"With subdialog"}),e.jsx(v,{style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:5},children:e.jsxs(h,{children:[e.jsxs(L,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Search"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsxs(j,{className:l.menu,...t,children:[e.jsx(c,{children:"Subdialog Foo"}),e.jsx(c,{children:"Subdialog Bar"}),e.jsx(c,{children:"Subdialog Baz"})]})]})})]}),e.jsx(c,{children:"Option"}),e.jsx(c,{children:"Option with a space"})]}),e.jsx(Mt,{style:{borderTop:"1px solid gray",margin:"2px 5px"}}),e.jsxs(ue,{className:l.group,children:[e.jsx(oe,{style:{fontSize:"1.2em"},children:"Section 2"}),e.jsxs(c,{textValue:"Copy",children:[e.jsx(r,{slot:"label",children:"Copy"}),e.jsx(r,{slot:"description",children:"Description"}),e.jsx(ce,{children:"⌘C"})]}),e.jsxs(c,{textValue:"Cut",children:[e.jsx(r,{slot:"label",children:"Cut"}),e.jsx(r,{slot:"description",children:"Description"}),e.jsx(ce,{children:"⌘X"})]}),e.jsxs(c,{textValue:"Paste",children:[e.jsx(r,{slot:"label",children:"Paste"}),e.jsx(r,{slot:"description",children:"Description"}),e.jsx(ce,{children:"⌘V"})]})]})]});function h(t){let{contains:s}=B({sensitivity:"base"}),i=(o,u)=>s(o,u);return e.jsx(f,{filter:i,...t})}const $={render:t=>e.jsx(h,{disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(L,{autoFocus:!0,"data-testid":"autocomplete-example",children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(wt,{...t})]})}),name:"Autocomplete complex static with textfield"},R={render:t=>e.jsx(h,{defaultValue:"Ba",disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,"data-testid":"autocomplete-example",children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(wt,{...t})]})}),name:"Autocomplete complex static with searchfield",parameters:{description:{data:"Note that on mobile, trying to type into the subdialog inputs may cause scrolling and thus cause the subdialog to close. Please test in landscape mode."}}};let ye=[{name:"Section 1",isSection:!0,children:[{name:"Command Palette"},{name:"Open View"}]},{name:"Section 2",isSection:!0,children:[{name:"Appearance",id:"appearance",children:[{name:"Sub Section 1",isSection:!0,children:[{name:"Move Primary Side Bar Right"},{name:"Activity Bar Position",id:"activity",isMenu:!0,children:[{name:"Default"},{name:"Top"},{name:"Bottom"},{name:"Hidden"},{name:"Subdialog test",id:"sub",children:[{name:"A"},{name:"B"},{name:"C"},{name:"D"}]},{name:"Submenu test",id:"sub2",isMenu:!0,children:[{name:"A"},{name:"B"},{name:"C"},{name:"D"}]}]},{name:"Panel Position",id:"position",children:[{name:"Top"},{name:"Left"},{name:"Right"},{name:"Bottom"}]}]}]},{name:"Editor Layout",id:"editor",children:[{name:"Sub Section 1",isSection:!0,children:[{name:"Split up"},{name:"Split down"},{name:"Split left"},{name:"Split right"}]},{name:"Sub Section 2",isSection:!0,children:[{name:"Single"},{name:"Two columns"},{name:"Three columns"},{name:"Two rows"},{name:"Three rows"}]}]}]}],be=t=>t.isMenu?e.jsxs(pe,{children:[e.jsx(c,{children:t.name},t.name),e.jsx(v,{className:l.popover,children:e.jsx(j,{items:t.children,className:l.menu,onAction:w(`${t.name} onAction`),children:s=>N(s)})})]}):e.jsxs(pe,{children:[e.jsx(c,{id:t.name,textValue:t.name,children:t.name}),e.jsx(v,{style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:5},children:e.jsxs(h,{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Search"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(j,{className:l.menu,items:t.children,onAction:w(`${t.name} onAction`),children:s=>N(s)})]})})]}),je=t=>e.jsx(c,{id:t.name,textValue:t.name,children:t.name}),N=t=>t.children?t.isSection?e.jsxs(ue,{className:l.group,id:t.name,items:t.children,children:[t.name!=null&&e.jsx(oe,{style:{fontSize:"1.2em"},children:t.name}),e.jsx(he,{items:t.children??[],children:s=>s.children?be(s):je(s)})]}):be(t):je(t);const H={render:t=>e.jsxs(e.Fragment,{children:[e.jsx("input",{}),e.jsx(h,{disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(j,{className:l.menu,items:ye,...t,children:s=>N(s)})]})}),e.jsx("input",{})]}),name:"Autocomplete, dynamic menu"},E={render:t=>e.jsx(h,{disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsxs(j,{className:l.menu,...t,children:[e.jsx(c,{onAction:w("Foo action"),children:"Foo"}),e.jsx(c,{onAction:w("Bar action"),children:"Bar"}),e.jsx(c,{onAction:w("Baz action"),children:"Baz"})]})]})}),name:"Autocomplete, onAction on menu items"};let te=[{id:"1",name:"Foo"},{id:"2",name:"Bar"},{id:"3",name:"Baz"}];const _={render:t=>e.jsx(h,{disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(j,{className:l.menu,items:te,disabledKeys:["2"],...t,children:s=>e.jsx(c,{id:s.id,children:s.name})})]})}),name:"Autocomplete, disabled key"},Qt=t=>{let s=Ct({async load({filterText:g}){return{items:await new Promise(It=>{setTimeout(()=>{It(g?te.filter(Vt=>{let re=Vt.name.toLowerCase();for(let ge of g.toLowerCase()){if(!re.includes(ge))return!1;re=re.replace(ge,"")}return!0}):te)},300)})}}}),{onSelectionChange:i,selectionMode:o,includeLoadState:u,escapeKeyBehavior:y,disableVirtualFocus:p}=t,T;return u&&(T=s.isLoading?()=>"Loading":()=>"No results found."),e.jsx(f,{inputValue:s.filterText,onInputChange:s.setFilterText,disableVirtualFocus:p,children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(M,{escapeKeyBehavior:y,renderEmptyState:T,items:u&&s.isLoading?[]:s.items,className:l.menu,onSelectionChange:i,selectionMode:o,children:g=>e.jsx(b,{children:g.name})})]})})},K={render:t=>e.jsx(Qt,{...t}),name:"Autocomplete, useAsync level filtering with load state",args:{includeLoadState:!0}},Yt=t=>{let{contains:s}=B({sensitivity:"case"}),i=(o,u)=>s(o,u);return e.jsx(f,{filter:i,disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(j,{className:l.menu,items:te,...t,children:o=>e.jsx(c,{id:o.id,children:o.name})})]})})},U={render:t=>e.jsx(Yt,{...t}),name:"Autocomplete, case sensitive filter"},X={render:t=>e.jsxs(ie,{children:[e.jsx(d,{children:"Open popover"}),e.jsx(v,{placement:"bottom start",style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:20,height:250},children:()=>e.jsx(h,{defaultInputValue:"Ba",disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsxs(M,{className:l.menu,...t,"aria-label":"test listbox with section",children:[e.jsxs(de,{className:l.group,children:[e.jsx(oe,{style:{fontSize:"1.2em"},children:"Section 1"}),e.jsx(b,{children:"Foo"}),e.jsx(b,{children:"Bar"}),e.jsx(b,{children:"Baz"}),e.jsx(b,{href:"http://google.com",children:"Google"})]}),e.jsx(Mt,{style:{borderTop:"1px solid gray",margin:"2px 5px"}}),e.jsxs(de,{className:l.group,"aria-label":"Section 2",children:[e.jsx(b,{children:"Copy"}),e.jsx(b,{children:"Paste"}),e.jsx(b,{children:"Cut"})]})]})]})})})]}),name:"Autocomplete with ListBox + Popover"};function Zt(t){let s=[];for(let p=0;p<1e4;p++)s.push({id:p,name:`Item ${p}`});let i=Ut({initialItems:s}),{onSelectionChange:o,selectionMode:u,escapeKeyBehavior:y}=t;return e.jsx(le,{layout:xe,layoutOptions:{rowHeight:25},children:e.jsx(M,{escapeKeyBehavior:y,onSelectionChange:o,selectionMode:u,className:l.menu,style:{height:200},"aria-label":"virtualized listbox",items:i.items,children:p=>e.jsx(b,{children:p.name})})})}const q={render:t=>e.jsxs(ie,{children:[e.jsx(d,{children:"Open popover"}),e.jsx(v,{placement:"bottom start",style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:20,height:250},children:()=>e.jsx(h,{disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(Zt,{...t})]})})})]}),name:"Autocomplete with ListBox + Popover, virtualized"};let se=[];for(let t=0;t<50;t++){let s=[];for(let i=0;i<50;i++)s.push({name:`Section ${t}, Item ${i}`,id:`item_${t}_${i}`});se.push({name:"Section "+t,id:`section_${t}`,children:s})}se=[{name:"Recently visited",id:"recent",children:[]}].concat(se);function kt(){let t=Jt({initialItems:se,getKey:i=>i.id,getChildren:i=>i.children||null}),s=i=>{t.move([...i][0],"recent",0)};return e.jsx(le,{layout:xe,layoutOptions:{rowHeight:25,headingHeight:25},children:e.jsx(M,{onSelectionChange:s,selectionMode:"single",className:l.menu,style:{height:200},"aria-label":"virtualized listbox",items:t.items,children:i=>e.jsxs(de,{id:i.value.id,className:l.group,children:[i.value.name!=null&&e.jsx(oe,{style:{fontSize:"1.2em"},children:i.value.name}),e.jsx(he,{items:i.children??[],children:o=>e.jsx(b,{id:o.value.id,children:o.value.name})})]})})})}const J={render:()=>e.jsxs(me,{children:[e.jsx(d,{children:"Open popover"}),e.jsx(v,{placement:"bottom start",style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:20,height:250},children:e.jsx(h,{children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(kt,{})]})})})]}),name:"Autocomplete in popover (menu trigger), shell example",argTypes:{selectionMode:{table:{disable:!0}}},parameters:{description:{data:"Menu is single selection so only the latest selected option will show the selected style"}}},Q={render:()=>e.jsxs(ie,{children:[e.jsx(d,{children:"Open popover"}),e.jsx(v,{placement:"bottom start",style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:20,height:250},children:()=>e.jsx(h,{children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(kt,{})]})})})]}),name:"Autocomplete in popover (dialog trigger), shell example",argTypes:{selectionMode:{table:{disable:!0}}},parameters:{description:{data:"Menu is single selection so only the latest selected option will show the selected style"}}},es=()=>{let{contains:t}=B({sensitivity:"base"});return e.jsxs(me,{children:[e.jsx(d,{"aria-label":"Menu",children:"☰"}),e.jsxs(v,{children:[e.jsx(d,{children:"First"}),e.jsx(d,{children:"Second"}),e.jsxs(f,{filter:t,children:[e.jsx(L,{autoFocus:!0,children:e.jsx(n,{})}),e.jsxs(j,{children:[e.jsx(A,{onAction:()=>console.log("open"),children:"Open"}),e.jsx(A,{onAction:()=>console.log("rename"),children:"Rename…"}),e.jsx(A,{onAction:()=>console.log("duplicate"),children:"Duplicate"}),e.jsx(A,{onAction:()=>console.log("share"),children:"Share…"}),e.jsx(A,{onAction:()=>console.log("delete"),children:"Delete…"})]})]})]})]})},ts=()=>{let{contains:t}=B({sensitivity:"base"});return e.jsxs(me,{children:[e.jsx(d,{"aria-label":"Menu",children:"☰"}),e.jsxs(v,{children:[e.jsxs(f,{filter:t,children:[e.jsx(L,{autoFocus:!0,children:e.jsx(n,{})}),e.jsxs(j,{children:[e.jsx(A,{onAction:()=>console.log("open"),children:"Open"}),e.jsx(A,{onAction:()=>console.log("rename"),children:"Rename…"}),e.jsx(A,{onAction:()=>console.log("duplicate"),children:"Duplicate"}),e.jsx(A,{onAction:()=>console.log("share"),children:"Share…"}),e.jsx(A,{onAction:()=>console.log("delete"),children:"Delete…"})]})]}),e.jsx(d,{children:"First"}),e.jsx(d,{children:"Second"})]})]})};function I(){return e.jsxs("div",{children:[e.jsx("input",{}),e.jsxs("div",{style:{display:"flex",gap:"200px"},children:[e.jsx(es,{}),e.jsx(ts,{})]}),e.jsx("input",{})]})}const Y={render:t=>e.jsxs(ie,{children:[e.jsx(d,{children:"Open popover"}),e.jsx(v,{placement:"bottom start",style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:20,height:250},children:e.jsx(h,{children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(j,{className:l.menu,items:ye,...t,children:s=>N(s)})]})})})]}),name:"Autocomplete in popover (dialog trigger), rendering dynamic autocomplete menu",argTypes:{selectionMode:{table:{disable:!0}}}};let ss=[...Array(100)].map((t,s)=>({id:s,name:`Item ${s}`}));const V=()=>e.jsxs(Pt,{style:{marginBottom:40},children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsxs(d,{children:[e.jsx(Gt,{}),e.jsx("span",{"aria-hidden":"true",style:{paddingLeft:5},children:"▼"})]}),e.jsx(v,{style:{background:"Canvas",border:"1px solid ButtonBorder",padding:5,boxSizing:"border-box",display:"flex"},children:e.jsxs(f,{filter:B({sensitivity:"base"}).contains,children:[e.jsx(x,{"aria-label":"Search",autoFocus:!0,style:{display:"flex",flexDirection:"column"},children:e.jsx(n,{})}),e.jsx(M,{items:ss,className:l.menu,style:{flex:1},children:t=>e.jsx(b,{children:t.name})})]})})]});let is=(t,s)=>{let i;return t.loadingState==="loading"?i=e.jsx(Xt,{style:{height:20,width:20,transform:"translate(-50%, -50%)"}}):t.loadingState==="idle"&&!s&&(i="No results"),e.jsx("div",{style:{height:30,width:"100%"},children:i})};const C=t=>{let[s,i]=Bt.useState(null),o=Ct({async load({signal:u,cursor:y,filterText:p}){y&&(y=y.replace(/^http:\/\//i,"https://")),await new Promise(F=>setTimeout(F,t.delay));let g=await(await fetch(y||`https://swapi.py4e.com/api/people/?search=${p}`,{signal:u})).json();return i(g.next),{items:g.results,cursor:g.next}}});return e.jsx(h,{disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(L,{autoFocus:!0,"data-testid":"autocomplete-example",children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(le,{layout:xe,layoutOptions:{rowHeight:50,padding:4,loaderHeight:30},children:e.jsxs(M,{...t,style:{height:400,width:100,border:"1px solid gray",background:"lightgray",overflow:"auto",padding:"unset",display:"flex"},"aria-label":"async virtualized listbox",renderEmptyState:()=>is(o,s),children:[e.jsx(he,{items:o.items,children:u=>e.jsx(b,{style:{backgroundColor:"lightgrey",border:"1px solid black",boxSizing:"border-box",height:"100%",width:"100%"},id:u.name,children:u.name})}),e.jsx(qt,{isLoading:o.loadingState==="loadingMore",onLoadMore:o.loadMore})]})})]})})};C.story={args:{delay:50}};const P=()=>e.jsx(h,{children:e.jsxs("div",{children:[e.jsxs(L,{autoFocus:!0,"data-testid":"autocomplete-example",children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{})]}),e.jsxs(Wt,{className:l.menu,style:{height:200,width:200},"aria-label":"test gridlist",children:[e.jsxs(ae,{children:[e.jsx(ne,{children:"Section 1"}),e.jsxs(S,{textValue:"Foo",children:["Foo ",e.jsx(d,{children:"Actions"})]}),e.jsxs(S,{textValue:"Bar",children:["Bar ",e.jsx(d,{children:"Actions"})]}),e.jsxs(S,{textValue:"Baz",children:["Baz ",e.jsx(d,{children:"Actions"})]})]}),e.jsxs(ae,{children:[e.jsx(ne,{children:"Section 2"}),e.jsxs(S,{textValue:"Charizard",children:["Charizard",e.jsx(d,{children:"Actions"})]}),e.jsxs(S,{textValue:"Blastoise",children:["Blastoise ",e.jsx(d,{children:"Actions"})]}),e.jsxs(S,{textValue:"Pikachu",children:["Pikachu ",e.jsx(d,{children:"Actions"})]}),e.jsxs(S,{textValue:"Venusaur",children:["Venusaur",e.jsx(d,{children:"Actions"})]})]}),e.jsxs(ae,{children:[e.jsx(ne,{children:"Section 3"}),e.jsxs(S,{textValue:"text value check",children:['textValue is "text value check" ',e.jsx(d,{children:"Actions"})]}),e.jsxs(S,{textValue:"Blah",children:["Blah ",e.jsx(d,{children:"Actions"})]})]})]})]})}),G=()=>e.jsx(h,{children:e.jsxs("div",{children:[e.jsxs(L,{autoFocus:!0,"data-testid":"autocomplete-example",children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{})]}),e.jsx(le,{layout:Kt,layoutOptions:{rowHeight:25,headingHeight:25,padding:10},children:e.jsxs(Nt,{"aria-label":"Files",selectionMode:"multiple",style:{height:400,width:400,overflow:"auto",scrollPaddingTop:25},children:[e.jsxs(zt,{style:{background:"var(--spectrum-gray-100)",width:"100%",height:"100%"},children:[e.jsx(z,{children:e.jsx(k,{slot:"selection"})}),e.jsx(z,{isRowHeader:!0,children:"Name"}),e.jsx(z,{children:"Type"}),e.jsx(z,{children:"Date Modified"})]}),e.jsxs(Ot,{children:[e.jsxs(O,{id:"1",style:{width:"inherit",height:"inherit"},children:[e.jsx(m,{children:e.jsx(k,{slot:"selection"})}),e.jsx(m,{children:"Games"}),e.jsx(m,{children:"File folder"}),e.jsx(m,{children:"6/7/2020"})]}),e.jsxs(O,{id:"2",style:{width:"inherit",height:"inherit"},children:[e.jsx(m,{children:e.jsx(k,{slot:"selection"})}),e.jsx(m,{children:"Program Files"}),e.jsx(m,{children:"File folder"}),e.jsx(m,{children:"4/7/2021"})]}),e.jsxs(O,{id:"3",style:{width:"inherit",height:"inherit"},children:[e.jsx(m,{children:e.jsx(k,{slot:"selection"})}),e.jsx(m,{children:"bootmgr"}),e.jsx(m,{children:"System file"}),e.jsx(m,{children:"11/20/2010"})]}),e.jsxs(O,{id:"4",style:{width:"inherit",height:"inherit"},children:[e.jsx(m,{children:e.jsx(k,{slot:"selection"})}),e.jsx(m,{children:"log.txt"}),e.jsx(m,{children:"Text Document"}),e.jsx(m,{children:"1/18/2016"})]})]})]})})]})}),W=()=>e.jsx(h,{children:e.jsxs("div",{children:[e.jsxs(L,{autoFocus:!0,"data-testid":"autocomplete-example",children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{})]}),e.jsxs(Dt,{children:[e.jsx(a,{children:"Categories"}),e.jsxs($t,{style:{display:"flex",gap:4},children:[e.jsx(D,{href:"https://nytimes.com",children:"News"}),e.jsx(D,{children:"Travel"}),e.jsx(D,{children:"Gaming"}),e.jsxs(Rt,{children:[e.jsx(D,{children:"Shopping"}),e.jsxs(Ht,{offset:5,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:5,borderRadius:4},children:[e.jsx(Et,{style:{transform:"translateX(-50%)"},children:e.jsx("svg",{width:"8",height:"8",style:{display:"block"},children:e.jsx("path",{d:"M0 0L4 4L8 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),"I am a tooltip"]})]})]})]})]})});function os(t){let{contains:s}=B({sensitivity:"base"}),i=(o,u,y)=>y.parentKey==="Section 1"&&o==="Open View"||y.parentKey==="Section 2"&&o==="Appearance"?!0:s(o,u);return e.jsx(f,{filter:i,disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(x,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(n,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(j,{className:l.menu,items:ye,...t,children:o=>N(o)})]})})}const Z={render:t=>e.jsx(os,{...t}),name:"Autocomplete, per node filtering",parameters:{description:{data:"It should never filter out Open View or Appearance"}}};let ve=[{id:1,name:"David"},{id:2,name:"Sam"},{id:3,name:"Julia"}];const ls=t=>{let[s,i]=Bt.useState(""),{contains:o}=B({sensitivity:"base"}),u=(p,T)=>{let g=T.lastIndexOf("@"),F="";return g>-1&&(F=s.slice(g+1)),o(p,F)},y=p=>{let T=s.lastIndexOf("@");T===-1&&(T=s.length);let g=ve.find(F=>F.id===p).name;i(s.slice(0,T).concat(g))};return e.jsx(f,{inputValue:s,onInputChange:i,filter:u,disableVirtualFocus:t.disableVirtualFocus,children:e.jsxs("div",{children:[e.jsxs(L,{autoFocus:!0,children:[e.jsx(a,{style:{display:"block"},children:"Test"}),e.jsx(_t,{}),e.jsx(r,{style:{display:"block"},slot:"description",children:"Please select an option below."})]}),e.jsx(M,{...t,className:l.menu,items:ve,"aria-label":"test listbox with sections",onAction:y,children:p=>e.jsx(b,{id:p.id,children:p.name})})]})})},ee={render:t=>e.jsx(ls,{...t}),name:"Autocomplete, user custom filterText (mentions)",parameters:{description:{data:"It should only filter if you type @, using the remainder of the string after the @ symbol as the filter text"}}};I.__docgenInfo={description:"",methods:[],displayName:"AutocompleteWithExtraButtons"};V.__docgenInfo={description:"",methods:[],displayName:"AutocompleteSelect"};C.__docgenInfo={description:"",methods:[],displayName:"AutocompleteWithAsyncListBox"};P.__docgenInfo={description:"",methods:[],displayName:"AutocompleteWithGridList"};G.__docgenInfo={description:"",methods:[],displayName:"AutocompleteWithTable"};W.__docgenInfo={description:"",methods:[],displayName:"AutocompleteWithTagGroup"};var Ae,Te,Se;$.parameters={...$.parameters,docs:{...(Ae=$.parameters)==null?void 0:Ae.docs,source:{originalSource:`{
  render: args => {
    return <AutocompleteWrapper disableVirtualFocus={args.disableVirtualFocus}>
        <div>
          <TextField autoFocus data-testid="autocomplete-example">
            <Label style={{
            display: 'block'
          }}>Test</Label>
            <Input />
            <Text style={{
            display: 'block'
          }} slot="description">Please select an option below.</Text>
          </TextField>
          <StaticMenu {...args} />
        </div>
      </AutocompleteWrapper>;
  },
  name: 'Autocomplete complex static with textfield'
}`,...(Se=(Te=$.parameters)==null?void 0:Te.docs)==null?void 0:Se.source}}};var fe,Le,Fe;R.parameters={...R.parameters,docs:{...(fe=R.parameters)==null?void 0:fe.docs,source:{originalSource:`{
  render: args => {
    return <AutocompleteWrapper defaultValue="Ba" disableVirtualFocus={args.disableVirtualFocus}>
        <div>
          <SearchField autoFocus data-testid="autocomplete-example">
            <Label style={{
            display: 'block'
          }}>Test</Label>
            <Input />
            <Text style={{
            display: 'block'
          }} slot="description">Please select an option below.</Text>
          </SearchField>
          <StaticMenu {...args} />
        </div>
      </AutocompleteWrapper>;
  },
  name: 'Autocomplete complex static with searchfield',
  parameters: {
    description: {
      data: 'Note that on mobile, trying to type into the subdialog inputs may cause scrolling and thus cause the subdialog to close. Please test in landscape mode.'
    }
  }
}`,...(Fe=(Le=R.parameters)==null?void 0:Le.docs)==null?void 0:Fe.source}}};var Me,Be,Ce;H.parameters={...H.parameters,docs:{...(Me=H.parameters)==null?void 0:Me.docs,source:{originalSource:`{
  render: args => {
    return <>
        <input />
        <AutocompleteWrapper disableVirtualFocus={args.disableVirtualFocus}>
          <div>
            <SearchField autoFocus>
              <Label style={{
              display: 'block'
            }}>Test</Label>
              <Input />
              <Text style={{
              display: 'block'
            }} slot="description">Please select an option below.</Text>
            </SearchField>
            <Menu className={styles.menu} items={dynamicAutocompleteSubdialog} {...args}>
              {item => dynamicRenderFuncSections(item)}
            </Menu>
          </div>
        </AutocompleteWrapper>
        <input />
      </>;
  },
  name: 'Autocomplete, dynamic menu'
}`,...(Ce=(Be=H.parameters)==null?void 0:Be.docs)==null?void 0:Ce.source}}};var we,ke,Ie;E.parameters={...E.parameters,docs:{...(we=E.parameters)==null?void 0:we.docs,source:{originalSource:`{
  render: args => {
    return <AutocompleteWrapper disableVirtualFocus={args.disableVirtualFocus}>
        <div>
          <SearchField autoFocus>
            <Label style={{
            display: 'block'
          }}>Test</Label>
            <Input />
            <Text style={{
            display: 'block'
          }} slot="description">Please select an option below.</Text>
          </SearchField>
          <Menu className={styles.menu} {...args}>
            <MyMenuItem onAction={action('Foo action')}>Foo</MyMenuItem>
            <MyMenuItem onAction={action('Bar action')}>Bar</MyMenuItem>
            <MyMenuItem onAction={action('Baz action')}>Baz</MyMenuItem>
          </Menu>
        </div>
      </AutocompleteWrapper>;
  },
  name: 'Autocomplete, onAction on menu items'
}`,...(Ie=(ke=E.parameters)==null?void 0:ke.docs)==null?void 0:Ie.source}}};var Ve,Pe,Ge;_.parameters={..._.parameters,docs:{...(Ve=_.parameters)==null?void 0:Ve.docs,source:{originalSource:`{
  render: args => {
    return <AutocompleteWrapper disableVirtualFocus={args.disableVirtualFocus}>
        <div>
          <SearchField autoFocus>
            <Label style={{
            display: 'block'
          }}>Test</Label>
            <Input />
            <Text style={{
            display: 'block'
          }} slot="description">Please select an option below.</Text>
          </SearchField>
          <Menu className={styles.menu} items={items} disabledKeys={['2']} {...args}>
            {(item: AutocompleteItem) => <MyMenuItem id={item.id}>{item.name}</MyMenuItem>}
          </Menu>
        </div>
      </AutocompleteWrapper>;
  },
  name: 'Autocomplete, disabled key'
}`,...(Ge=(Pe=_.parameters)==null?void 0:Pe.docs)==null?void 0:Ge.source}}};var We,Ne,ze;K.parameters={...K.parameters,docs:{...(We=K.parameters)==null?void 0:We.docs,source:{originalSource:`{
  render: args => {
    return <AsyncExample {...args} />;
  },
  name: 'Autocomplete, useAsync level filtering with load state',
  args: {
    includeLoadState: true
  }
}`,...(ze=(Ne=K.parameters)==null?void 0:Ne.docs)==null?void 0:ze.source}}};var Oe,De,$e;U.parameters={...U.parameters,docs:{...(Oe=U.parameters)==null?void 0:Oe.docs,source:{originalSource:`{
  render: args => {
    return <CaseSensitiveFilter {...args} />;
  },
  name: 'Autocomplete, case sensitive filter'
}`,...($e=(De=U.parameters)==null?void 0:De.docs)==null?void 0:$e.source}}};var Re,He,Ee;X.parameters={...X.parameters,docs:{...(Re=X.parameters)==null?void 0:Re.docs,source:{originalSource:`{
  render: args => {
    return <DialogTrigger>
        <Button>
          Open popover
        </Button>
        <Popover placement="bottom start" style={{
        background: 'Canvas',
        color: 'CanvasText',
        border: '1px solid gray',
        padding: 20,
        height: 250
      }}>
          {() => <AutocompleteWrapper defaultInputValue="Ba" disableVirtualFocus={args.disableVirtualFocus}>
              <div>
                <SearchField autoFocus>
                  <Label style={{
                display: 'block'
              }}>Test</Label>
                  <Input />
                  <Text style={{
                display: 'block'
              }} slot="description">Please select an option below.</Text>
                </SearchField>
                <ListBox className={styles.menu} {...args} aria-label="test listbox with section">
                  <ListBoxSection className={styles.group}>
                    <Header style={{
                  fontSize: '1.2em'
                }}>Section 1</Header>
                    <MyListBoxItem>Foo</MyListBoxItem>
                    <MyListBoxItem>Bar</MyListBoxItem>
                    <MyListBoxItem>Baz</MyListBoxItem>
                    <MyListBoxItem href="http://google.com">Google</MyListBoxItem>
                  </ListBoxSection>
                  <Separator style={{
                borderTop: '1px solid gray',
                margin: '2px 5px'
              }} />
                  <ListBoxSection className={styles.group} aria-label="Section 2">
                    <MyListBoxItem>Copy</MyListBoxItem>
                    <MyListBoxItem>Paste</MyListBoxItem>
                    <MyListBoxItem>Cut</MyListBoxItem>
                  </ListBoxSection>
                </ListBox>
              </div>
            </AutocompleteWrapper>}
        </Popover>
      </DialogTrigger>;
  },
  name: 'Autocomplete with ListBox + Popover'
}`,...(Ee=(He=X.parameters)==null?void 0:He.docs)==null?void 0:Ee.source}}};var _e,Ke,Ue;q.parameters={...q.parameters,docs:{...(_e=q.parameters)==null?void 0:_e.docs,source:{originalSource:`{
  render: args => {
    return <DialogTrigger>
        <Button>
          Open popover
        </Button>
        <Popover placement="bottom start" style={{
        background: 'Canvas',
        color: 'CanvasText',
        border: '1px solid gray',
        padding: 20,
        height: 250
      }}>
          {() => <AutocompleteWrapper disableVirtualFocus={args.disableVirtualFocus}>
              <div>
                <SearchField autoFocus>
                  <Label style={{
                display: 'block'
              }}>Test</Label>
                  <Input />
                  <Text style={{
                display: 'block'
              }} slot="description">Please select an option below.</Text>
                </SearchField>
                <VirtualizedListBox {...args} />
              </div>
            </AutocompleteWrapper>}
        </Popover>
      </DialogTrigger>;
  },
  name: 'Autocomplete with ListBox + Popover, virtualized'
}`,...(Ue=(Ke=q.parameters)==null?void 0:Ke.docs)==null?void 0:Ue.source}}};var Xe,qe,Je;J.parameters={...J.parameters,docs:{...(Xe=J.parameters)==null?void 0:Xe.docs,source:{originalSource:`{
  render: () => {
    return <MenuTrigger>
        <Button>
          Open popover
        </Button>
        <Popover placement="bottom start" style={{
        background: 'Canvas',
        color: 'CanvasText',
        border: '1px solid gray',
        padding: 20,
        height: 250
      }}>
          <AutocompleteWrapper>
            <div>
              <SearchField autoFocus>
                <Label style={{
                display: 'block'
              }}>Test</Label>
                <Input />
                <Text style={{
                display: 'block'
              }} slot="description">Please select an option below.</Text>
              </SearchField>
              <ShellExample />
            </div>
          </AutocompleteWrapper>
        </Popover>
      </MenuTrigger>;
  },
  name: 'Autocomplete in popover (menu trigger), shell example',
  argTypes: {
    selectionMode: {
      table: {
        disable: true
      }
    }
  },
  parameters: {
    description: {
      data: 'Menu is single selection so only the latest selected option will show the selected style'
    }
  }
}`,...(Je=(qe=J.parameters)==null?void 0:qe.docs)==null?void 0:Je.source}}};var Qe,Ye,Ze;Q.parameters={...Q.parameters,docs:{...(Qe=Q.parameters)==null?void 0:Qe.docs,source:{originalSource:`{
  render: () => {
    return <DialogTrigger>
        <Button>
          Open popover
        </Button>
        <Popover placement="bottom start" style={{
        background: 'Canvas',
        color: 'CanvasText',
        border: '1px solid gray',
        padding: 20,
        height: 250
      }}>
          {() => <AutocompleteWrapper>
              <div>
                <SearchField autoFocus>
                  <Label style={{
                display: 'block'
              }}>Test</Label>
                  <Input />
                  <Text style={{
                display: 'block'
              }} slot="description">Please select an option below.</Text>
                </SearchField>
                <ShellExample />
              </div>
            </AutocompleteWrapper>}
        </Popover>
      </DialogTrigger>;
  },
  name: 'Autocomplete in popover (dialog trigger), shell example',
  argTypes: {
    selectionMode: {
      table: {
        disable: true
      }
    }
  },
  parameters: {
    description: {
      data: 'Menu is single selection so only the latest selected option will show the selected style'
    }
  }
}`,...(Ze=(Ye=Q.parameters)==null?void 0:Ye.docs)==null?void 0:Ze.source}}};var et,tt,st;I.parameters={...I.parameters,docs:{...(et=I.parameters)==null?void 0:et.docs,source:{originalSource:`function AutocompleteWithExtraButtons(): React.ReactElement {
  return <div>
      <input />
      <div style={{
      display: 'flex',
      gap: '200px'
    }}>
        <MyMenu />
        <MyMenu2 />
      </div>
      <input />
    </div>;
}`,...(st=(tt=I.parameters)==null?void 0:tt.docs)==null?void 0:st.source}}};var it,ot,lt;Y.parameters={...Y.parameters,docs:{...(it=Y.parameters)==null?void 0:it.docs,source:{originalSource:`{
  render: args => {
    return <DialogTrigger>
        <Button>
          Open popover
        </Button>
        <Popover placement="bottom start" style={{
        background: 'Canvas',
        color: 'CanvasText',
        border: '1px solid gray',
        padding: 20,
        height: 250
      }}>
          <AutocompleteWrapper>
            <div>
              <SearchField autoFocus>
                <Label style={{
                display: 'block'
              }}>Test</Label>
                <Input />
                <Text style={{
                display: 'block'
              }} slot="description">Please select an option below.</Text>
              </SearchField>
              <Menu className={styles.menu} items={dynamicAutocompleteSubdialog} {...args}>
                {item => dynamicRenderFuncSections(item)}
              </Menu>
            </div>
          </AutocompleteWrapper>
        </Popover>
      </DialogTrigger>;
  },
  name: 'Autocomplete in popover (dialog trigger), rendering dynamic autocomplete menu',
  argTypes: {
    selectionMode: {
      table: {
        disable: true
      }
    }
  }
}`,...(lt=(ot=Y.parameters)==null?void 0:ot.docs)==null?void 0:lt.source}}};var rt,at,nt;V.parameters={...V.parameters,docs:{...(rt=V.parameters)==null?void 0:rt.docs,source:{originalSource:`(): React.ReactElement => <Select style={{
  marginBottom: 40
}}>
    <Label style={{
    display: 'block'
  }}>Test</Label>
    <Button>
      <SelectValue />
      <span aria-hidden="true" style={{
      paddingLeft: 5
    }}>▼</span>
    </Button>
    <Popover style={{
    background: 'Canvas',
    border: '1px solid ButtonBorder',
    padding: 5,
    boxSizing: 'border-box',
    display: 'flex'
  }}>
      <Autocomplete filter={useFilter({
      sensitivity: 'base'
    }).contains}>
        <SearchField aria-label="Search" autoFocus style={{
        display: 'flex',
        flexDirection: 'column'
      }}>
          <Input />
        </SearchField>
        <ListBox items={manyItems} className={styles.menu} style={{
        flex: 1
      }}>
          {item => <MyListBoxItem>{item.name}</MyListBoxItem>}
        </ListBox>
      </Autocomplete>
    </Popover>
  </Select>`,...(nt=(at=V.parameters)==null?void 0:at.docs)==null?void 0:nt.source}}};var ct,dt,ut;C.parameters={...C.parameters,docs:{...(ct=C.parameters)==null?void 0:ct.docs,source:{originalSource:`args => {
  let [cursor, setCursor] = useState(null);
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
      setCursor(json.next);
      return {
        items: json.results,
        cursor: json.next
      };
    }
  });
  return <AutocompleteWrapper disableVirtualFocus={args.disableVirtualFocus}>
      <div>
        <TextField autoFocus data-testid="autocomplete-example">
          <Label style={{
          display: 'block'
        }}>Test</Label>
          <Input />
          <Text style={{
          display: 'block'
        }} slot="description">Please select an option below.</Text>
        </TextField>
        <Virtualizer layout={ListLayout} layoutOptions={{
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
        }} aria-label="async virtualized listbox" renderEmptyState={() => renderEmptyState(list, cursor)}>
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
        </Virtualizer>
      </div>
    </AutocompleteWrapper>;
}`,...(ut=(dt=C.parameters)==null?void 0:dt.docs)==null?void 0:ut.source}}};var pt,mt,ht;P.parameters={...P.parameters,docs:{...(pt=P.parameters)==null?void 0:pt.docs,source:{originalSource:`() => {
  return <AutocompleteWrapper>
      <div>
        <TextField autoFocus data-testid="autocomplete-example">
          <Label style={{
          display: 'block'
        }}>Test</Label>
          <Input />
        </TextField>
        <GridList className={styles.menu} style={{
        height: 200,
        width: 200
      }} aria-label="test gridlist">
          <GridListSection>
            <GridListHeader>Section 1</GridListHeader>
            <MyGridListItem textValue="Foo">Foo <Button>Actions</Button></MyGridListItem>
            <MyGridListItem textValue="Bar">Bar <Button>Actions</Button></MyGridListItem>
            <MyGridListItem textValue="Baz">Baz <Button>Actions</Button></MyGridListItem>
          </GridListSection>
          <GridListSection>
            <GridListHeader>Section 2</GridListHeader>
            <MyGridListItem textValue="Charizard">Charizard<Button>Actions</Button></MyGridListItem>
            <MyGridListItem textValue="Blastoise">Blastoise <Button>Actions</Button></MyGridListItem>
            <MyGridListItem textValue="Pikachu">Pikachu <Button>Actions</Button></MyGridListItem>
            <MyGridListItem textValue="Venusaur">Venusaur<Button>Actions</Button></MyGridListItem>
          </GridListSection>
          <GridListSection>
            <GridListHeader>Section 3</GridListHeader>
            <MyGridListItem textValue="text value check">textValue is "text value check" <Button>Actions</Button></MyGridListItem>
            <MyGridListItem textValue="Blah">Blah <Button>Actions</Button></MyGridListItem>
          </GridListSection>
        </GridList>
      </div>
    </AutocompleteWrapper>;
}`,...(ht=(mt=P.parameters)==null?void 0:mt.docs)==null?void 0:ht.source}}};var xt,yt,gt;G.parameters={...G.parameters,docs:{...(xt=G.parameters)==null?void 0:xt.docs,source:{originalSource:`() => {
  return <AutocompleteWrapper>
      <div>
        <TextField autoFocus data-testid="autocomplete-example">
          <Label style={{
          display: 'block'
        }}>Test</Label>
          <Input />
        </TextField>
        <Virtualizer layout={TableLayout} layoutOptions={{
        rowHeight: 25,
        headingHeight: 25,
        padding: 10
      }}>
          <Table aria-label="Files" selectionMode="multiple" style={{
          height: 400,
          width: 400,
          overflow: 'auto',
          scrollPaddingTop: 25
        }}>
            <TableHeader style={{
            background: 'var(--spectrum-gray-100)',
            width: '100%',
            height: '100%'
          }}>
              <Column>
                <MyCheckbox slot="selection" />
              </Column>
              <Column isRowHeader>Name</Column>
              <Column>Type</Column>
              <Column>Date Modified</Column>
            </TableHeader>
            <TableBody>
              <Row id="1" style={{
              width: 'inherit',
              height: 'inherit'
            }}>
                <Cell>
                  <MyCheckbox slot="selection" />
                </Cell>
                <Cell>Games</Cell>
                <Cell>File folder</Cell>
                <Cell>6/7/2020</Cell>
              </Row>
              <Row id="2" style={{
              width: 'inherit',
              height: 'inherit'
            }}>
                <Cell>
                  <MyCheckbox slot="selection" />
                </Cell>
                <Cell>Program Files</Cell>
                <Cell>File folder</Cell>
                <Cell>4/7/2021</Cell>
              </Row>
              <Row id="3" style={{
              width: 'inherit',
              height: 'inherit'
            }}>
                <Cell>
                  <MyCheckbox slot="selection" />
                </Cell>
                <Cell>bootmgr</Cell>
                <Cell>System file</Cell>
                <Cell>11/20/2010</Cell>
              </Row>
              <Row id="4" style={{
              width: 'inherit',
              height: 'inherit'
            }}>
                <Cell>
                  <MyCheckbox slot="selection" />
                </Cell>
                <Cell>log.txt</Cell>
                <Cell>Text Document</Cell>
                <Cell>1/18/2016</Cell>
              </Row>
            </TableBody>
          </Table>
        </Virtualizer>
      </div>
    </AutocompleteWrapper>;
}`,...(gt=(yt=G.parameters)==null?void 0:yt.docs)==null?void 0:gt.source}}};var bt,jt,vt;W.parameters={...W.parameters,docs:{...(bt=W.parameters)==null?void 0:bt.docs,source:{originalSource:`() => {
  return <AutocompleteWrapper>
      <div>
        <TextField autoFocus data-testid="autocomplete-example">
          <Label style={{
          display: 'block'
        }}>Test</Label>
          <Input />
        </TextField>
        <TagGroup>
          <Label>Categories</Label>
          <TagList style={{
          display: 'flex',
          gap: 4
        }}>
            <MyTag href="https://nytimes.com">News</MyTag>
            <MyTag>Travel</MyTag>
            <MyTag>Gaming</MyTag>
            <TooltipTrigger>
              <MyTag>Shopping</MyTag>
              <Tooltip offset={5} style={{
              background: 'Canvas',
              color: 'CanvasText',
              border: '1px solid gray',
              padding: 5,
              borderRadius: 4
            }}>
                <OverlayArrow style={{
                transform: 'translateX(-50%)'
              }}>
                  <svg width="8" height="8" style={{
                  display: 'block'
                }}>
                    <path d="M0 0L4 4L8 0" fill="white" strokeWidth={1} stroke="gray" />
                  </svg>
                </OverlayArrow>
                I am a tooltip
              </Tooltip>
            </TooltipTrigger>
          </TagList>
        </TagGroup>
      </div>
    </AutocompleteWrapper>;
}`,...(vt=(jt=W.parameters)==null?void 0:jt.docs)==null?void 0:vt.source}}};var At,Tt,St;Z.parameters={...Z.parameters,docs:{...(At=Z.parameters)==null?void 0:At.docs,source:{originalSource:`{
  render: args => <AutocompleteNodeFiltering {...args} />,
  name: 'Autocomplete, per node filtering',
  parameters: {
    description: {
      data: 'It should never filter out Open View or Appearance'
    }
  }
}`,...(St=(Tt=Z.parameters)==null?void 0:Tt.docs)==null?void 0:St.source}}};var ft,Lt,Ft;ee.parameters={...ee.parameters,docs:{...(ft=ee.parameters)==null?void 0:ft.docs,source:{originalSource:`{
  render: args => <UserCustomFiltering {...args} />,
  name: 'Autocomplete, user custom filterText (mentions)',
  parameters: {
    description: {
      data: 'It should only filter if you type @, using the remainder of the string after the @ symbol as the filter text'
    }
  }
}`,...(Ft=(Lt=ee.parameters)==null?void 0:Lt.docs)==null?void 0:Ft.source}}};const Fs=["AutocompleteExample","AutocompleteSearchfield","AutocompleteMenuDynamic","AutocompleteOnActionOnMenuItems","AutocompleteDisabledKeys","AutocompleteAsyncLoadingExample","AutocompleteCaseSensitive","AutocompleteWithListbox","AutocompleteWithVirtualizedListbox","AutocompleteInPopover","AutocompleteInPopoverDialogTrigger","AutocompleteWithExtraButtons","AutocompleteMenuInPopoverDialogTrigger","AutocompleteSelect","AutocompleteWithAsyncListBox","AutocompleteWithGridList","AutocompleteWithTable","AutocompleteWithTagGroup","AutocompletePreserveFirstSectionStory","AutocompleteUserCustomFiltering"];export{K as AutocompleteAsyncLoadingExample,U as AutocompleteCaseSensitive,_ as AutocompleteDisabledKeys,$ as AutocompleteExample,J as AutocompleteInPopover,Q as AutocompleteInPopoverDialogTrigger,H as AutocompleteMenuDynamic,Y as AutocompleteMenuInPopoverDialogTrigger,E as AutocompleteOnActionOnMenuItems,Z as AutocompletePreserveFirstSectionStory,R as AutocompleteSearchfield,V as AutocompleteSelect,ee as AutocompleteUserCustomFiltering,C as AutocompleteWithAsyncListBox,I as AutocompleteWithExtraButtons,P as AutocompleteWithGridList,X as AutocompleteWithListbox,G as AutocompleteWithTable,W as AutocompleteWithTagGroup,q as AutocompleteWithVirtualizedListbox,Fs as __namedExportsOrder,Ls as default};
