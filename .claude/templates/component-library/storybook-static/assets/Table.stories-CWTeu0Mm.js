import{j as e}from"./jsx-runtime-CDt2p4po.js";import{a as ie}from"./index-B-lxVbXh.js";import{bc as yt,at as gt,az as v,bd as ae,be as ft,bf as bt,k as y,bg as I,l as g,C as m,m as b,R as p,n as o,D as xt,B as R,aw as wt,ax as jt,a4 as Tt,E as Ct,X as vt,h as Z,V as U,e as St,P as Rt,M as It,bh as kt,av as zt,b6 as ee,bi as Ht}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{r as B,R as re}from"./index-GiUgBvb1.js";import{a as Lt,d as k,b as te,$ as se}from"./ListLayout-8Q9Kcx4Y.js";import{u as oe}from"./useDragAndDrop--5mYXGU7.js";import{M as Mt,L as mt}from"./utils-N1pTmi3h.js";import{s as Dt}from"./index.module-B9nxguEg.js";/* empty css               */const he=48;class Pt extends Lt{get collection(){return this.virtualizer.collection}columnsChanged(t,a){return!a||t.columns!==a.columns&&t.columns.length!==a.columns.length||t.columns.some((i,l)=>i.key!==a.columns[l].key||i.props.width!==a.columns[l].props.width||i.props.minWidth!==a.columns[l].props.minWidth||i.props.maxWidth!==a.columns[l].props.maxWidth)}shouldInvalidateLayoutOptions(t,a){return t.columnWidths!==a.columnWidths||super.shouldInvalidateLayoutOptions(t,a)}update(t){var a;let i=this.virtualizer.collection;if(!((a=t.layoutOptions)===null||a===void 0)&&a.columnWidths){for(const[l,r]of t.layoutOptions.columnWidths)if(this.columnWidths.get(l)!==r){this.columnWidths=t.layoutOptions.columnWidths,t.sizeChanged=!0;break}}else if(t.sizeChanged||this.columnsChanged(i,this.lastCollection)){let l=new yt({});this.columnWidths=l.buildColumnWidths(this.virtualizer.visibleRect.width-this.padding*2,i,new Map),t.sizeChanged=!0}super.update(t)}buildCollection(){var t;this.stickyColumnIndices=[];let a=this.virtualizer.collection;if(((t=a.head)===null||t===void 0?void 0:t.key)===-1)return[];for(let r of a.columns)(this.isStickyColumn(r)||a.rowHeaderColumnKeys.has(r.key))&&this.stickyColumnIndices.push(r.index);let i=this.buildTableHeader();this.layoutNodes.set(i.layoutInfo.key,i);let l=this.buildBody(i.layoutInfo.rect.maxY+this.gap);return this.lastPersistedKeys=null,l.layoutInfo.rect.width=Math.max(i.layoutInfo.rect.width,l.layoutInfo.rect.width),this.contentSize=new gt(l.layoutInfo.rect.width+this.padding*2,l.layoutInfo.rect.maxY+this.padding),[i,l]}buildTableHeader(){var t;let a=this.virtualizer.collection,i=new v(this.padding,this.padding,0,0);var l;let r=new k("header",(l=(t=a.head)===null||t===void 0?void 0:t.key)!==null&&l!==void 0?l:"header",i);r.isSticky=!0,r.zIndex=1;let s=this.padding,d=0,c=[];for(let h of a.headerRows){let u=this.buildChild(h,this.padding,s,r.key);u.layoutInfo.parentKey=r.key,s=u.layoutInfo.rect.maxY,d=Math.max(d,u.layoutInfo.rect.width),u.index=c.length,c.push(u)}return i.width=d,i.height=s-this.padding,{layoutInfo:r,children:c,validRect:r.rect,node:a.head}}buildHeaderRow(t,a,i){let l=new v(a,i,0,0),r=new k("headerrow",t.key,l),s=0,d=[];for(let c of ae(t,this.virtualizer.collection)){let h=this.buildChild(c,a,i,r.key);h.layoutInfo.parentKey=r.key,a=h.layoutInfo.rect.maxX,s=Math.max(s,h.layoutInfo.rect.height),h.index=d.length,d.push(h)}for(let[c,h]of d.entries())h.layoutInfo.zIndex=d.length-c+1;return this.setChildHeights(d,s),l.height=s,l.width=a-l.x,{layoutInfo:r,children:d,validRect:l,node:t}}setChildHeights(t,a){for(let i of t)i.layoutInfo.rect.height!==a&&(i.layoutInfo=i.layoutInfo.copy(),i.layoutInfo.rect.height=a)}getRenderedColumnWidth(t){let a=this.virtualizer.collection;var i;let l=(i=t.colSpan)!==null&&i!==void 0?i:1;var r;let s=(r=t.colIndex)!==null&&r!==void 0?r:t.index,d=0;for(let h=s;h<s+l;h++){let u=a.columns[h];var c;(u==null?void 0:u.key)!=null&&(d+=(c=this.columnWidths.get(u.key))!==null&&c!==void 0?c:0)}return d}getEstimatedHeight(t,a,i,l){let r=!1;if(i==null){let s=this.layoutNodes.get(t.key);s?(i=s.layoutInfo.rect.height,r=t!==s.node||a!==s.layoutInfo.rect.width||s.layoutInfo.estimatedSize):(i=l??he,r=!0)}return{height:i,isEstimated:r}}getEstimatedRowHeight(){var t,a;return(a=(t=this.rowHeight)!==null&&t!==void 0?t:this.estimatedRowHeight)!==null&&a!==void 0?a:he}buildColumn(t,a,i){let l=this.getRenderedColumnWidth(t);var r,s;let{height:d,isEstimated:c}=this.getEstimatedHeight(t,l,(r=this.headingHeight)!==null&&r!==void 0?r:this.rowHeight,(s=this.estimatedHeadingHeight)!==null&&s!==void 0?s:this.estimatedRowHeight),h=new v(a,i,l,d),u=new k(t.type,t.key,h);return u.isSticky=this.isStickyColumn(t),u.zIndex=u.isSticky?2:1,u.estimatedSize=c,{layoutInfo:u,children:[],validRect:u.rect,node:t}}isStickyColumn(t){return!1}buildBody(t){let a=this.virtualizer.collection,i=new v(this.padding,t,0,0),l=new k("rowgroup",a.body.key,i),r=t,s=0,d=0,c=[],h=this.getEstimatedRowHeight()+this.gap,u=ae(a.body,a);for(let X of u){if(t+h<this.requestedRect.y&&!this.isValid(X,t)){t+=h,s++;continue}let C=this.buildChild(X,this.padding,t,l.key);if(C.layoutInfo.parentKey=l.key,C.index=c.length,t=C.layoutInfo.rect.maxY+this.gap,d=Math.max(d,C.layoutInfo.rect.width),c.push(C),t>this.requestedRect.maxY){var f;let pt=a.size-(c.length+s),Q=ft(u);if(t+=pt*h,(Q==null?void 0:Q.type)==="loader"&&((f=c.at(-1))===null||f===void 0?void 0:f.layoutInfo.type)!=="loader"){let _=this.buildChild(Q,this.padding,t,l.key);_.layoutInfo.parentKey=l.key,_.index=a.size,d=Math.max(d,_.layoutInfo.rect.width),c.push(_),t=_.layoutInfo.rect.maxY}break}}return(a==null?void 0:a.size)===0?t=this.virtualizer.visibleRect.maxY:t-=this.gap,i.width=d,i.height=t-r,{layoutInfo:l,children:c,validRect:l.rect.intersection(this.requestedRect),node:a.body}}buildNode(t,a,i){switch(t.type){case"headerrow":return this.buildHeaderRow(t,a,i);case"item":return this.buildRow(t,a,i);case"column":case"placeholder":return this.buildColumn(t,a,i);case"cell":return this.buildCell(t,a,i);case"loader":return this.buildLoader(t,a,i);default:throw new Error("Unknown node type "+t.type)}}buildRow(t,a,i){var l;let r=this.virtualizer.collection,s=new v(a,i,0,0),d=new k("row",t.key,s),c=[],h=0;for(let f of ae(t,r))if(f.type==="cell")if(a>this.requestedRect.maxX){let w=this.layoutNodes.get(f.key);if(w)w.layoutInfo.rect.x=a,a+=w.layoutInfo.rect.width;else break}else{let w=this.buildChild(f,a,i,d.key);a=w.layoutInfo.rect.maxX,h=Math.max(h,w.layoutInfo.rect.height),w.index=c.length,c.push(w)}this.setChildHeights(c,h);var u;return s.width=this.layoutNodes.get((u=(l=r.head)===null||l===void 0?void 0:l.key)!==null&&u!==void 0?u:"header").layoutInfo.rect.width,s.height=h,{layoutInfo:d,children:c,validRect:s.intersection(this.requestedRect),node:t}}buildCell(t,a,i){let l=this.getRenderedColumnWidth(t),{height:r,isEstimated:s}=this.getEstimatedHeight(t,l,this.rowHeight,this.estimatedRowHeight),d=new v(a,i,l,r),c=new k(t.type,t.key,d);return c.isSticky=this.isStickyColumn(t),c.zIndex=c.isSticky?2:1,c.estimatedSize=s,{layoutInfo:c,children:[],validRect:d,node:t}}getVisibleLayoutInfos(t){if(t.height>1){let i=this.getEstimatedRowHeight();t.y=Math.floor(t.y/i)*i,t.height=Math.ceil(t.height/i)*i}this.layoutIfNeeded(t);let a=[];this.buildPersistedIndices();for(let i of this.rootNodes)a.push(i.layoutInfo),this.addVisibleLayoutInfos(a,i,t);return a}addVisibleLayoutInfos(t,a,i){if(!(!a.children||a.children.length===0))switch(a.layoutInfo.type){case"header":for(let l of a.children)t.push(l.layoutInfo),this.addVisibleLayoutInfos(t,l,i);break;case"rowgroup":{let l=this.binarySearch(a.children,i.topLeft,"y"),r=this.binarySearch(a.children,i.bottomRight,"y"),s=this.persistedIndices.get(a.layoutInfo.key),d=0;for(;s&&d<s.length&&s[d]<l;){let h=s[d];h<a.children.length&&(t.push(a.children[h].layoutInfo),this.addVisibleLayoutInfos(t,a.children[h],i)),d++}for(let h=l;h<=r;h++){for(;s&&d<s.length&&s[d]<h;)d++;t.push(a.children[h].layoutInfo),this.addVisibleLayoutInfos(t,a.children[h],i)}for(;s&&d<s.length;){let h=s[d++];h<a.children.length&&(t.push(a.children[h].layoutInfo),this.addVisibleLayoutInfos(t,a.children[h],i))}let c=a.children.at(-1);(c==null?void 0:c.layoutInfo.type)==="loader"&&t.push(c.layoutInfo);break}case"headerrow":case"row":{let l=this.binarySearch(a.children,i.topLeft,"x"),r=this.binarySearch(a.children,i.topRight,"x"),s=0,d=this.persistedIndices.get(a.layoutInfo.key)||this.stickyColumnIndices;for(;s<d.length&&d[s]<l;){let c=d[s];c<a.children.length&&t.push(a.children[c].layoutInfo),s++}for(let c=l;c<=r;c++){for(;s<d.length&&d[s]<c;)s++;t.push(a.children[c].layoutInfo)}for(;s<d.length;){let c=d[s++];c<a.children.length&&t.push(a.children[c].layoutInfo)}break}default:throw new Error("Unknown node type "+a.layoutInfo.type)}}binarySearch(t,a,i){let l=0,r=t.length-1;for(;l<=r;){let s=l+r>>1,d=t[s];if(i==="x"&&d.layoutInfo.rect.maxX<=a.x||i==="y"&&d.layoutInfo.rect.maxY<=a.y)l=s+1;else if(i==="x"&&d.layoutInfo.rect.x>a.x||i==="y"&&d.layoutInfo.rect.y>a.y)r=s-1;else return s}return Math.max(0,Math.min(t.length-1,l))}buildPersistedIndices(){if(this.virtualizer.persistedKeys!==this.lastPersistedKeys){this.lastPersistedKeys=this.virtualizer.persistedKeys,this.persistedIndices.clear();for(let l of this.virtualizer.persistedKeys){var t;let r=(t=this.layoutNodes.get(l))===null||t===void 0?void 0:t.layoutInfo;for(;r&&r.parentKey;){var a,i;let s=this.virtualizer.collection.getItem(r.key),d=this.persistedIndices.get(r.parentKey);d||(d=(s==null?void 0:s.type)==="cell"||(s==null?void 0:s.type)==="column"?[...this.stickyColumnIndices]:[],this.persistedIndices.set(r.parentKey,d));let c=(a=this.layoutNodes.get(r.key))===null||a===void 0?void 0:a.index;c!=null&&!d.includes(c)&&d.push(c),r=(i=this.layoutNodes.get(r.parentKey))===null||i===void 0?void 0:i.layoutInfo}}for(let l of this.persistedIndices.values())l.sort((r,s)=>r-s)}}getDropTargetFromPoint(t,a,i){t+=this.virtualizer.visibleRect.x,a+=this.virtualizer.visibleRect.y;let l=new v(t,Math.max(0,a-this.gap),1,Math.max(1,this.gap*2)),r=this.getVisibleLayoutInfos(l),s=null,d=1/0;for(let f of r){if(f.type!=="row"||!f.rect.intersects(l))continue;let w=Math.abs(f.rect.y-a),X=Math.abs(f.rect.maxY-a),C=Math.min(w,X);C<d&&(d=C,s=f.key)}if(s==null||this.virtualizer.collection.size===0)return{type:"root"};let c=this.getLayoutInfo(s);if(!c)return null;let h=c.rect,u={type:"item",key:c.key,dropPosition:"on"};return i(u)?a<=h.y+10&&i({...u,dropPosition:"before"})?u.dropPosition="before":a>=h.maxY-10&&i({...u,dropPosition:"after"})&&(u.dropPosition="after"):a<=h.y+h.height/2&&i({...u,dropPosition:"before"})?u.dropPosition="before":i({...u,dropPosition:"after"})&&(u.dropPosition="after"),u}getDropTargetLayoutInfo(t){let a=super.getDropTargetLayoutInfo(t);return a.parentKey=this.virtualizer.collection.body.key,a}constructor(t){super(t),this.lastCollection=null,this.columnWidths=new Map,this.lastPersistedKeys=null,this.persistedIndices=new Map,this.stickyColumnIndices=[]}}class J extends Pt{useLayoutOptions(){let t=B.useContext(bt);return B.useMemo(()=>({columnWidths:t==null?void 0:t.columnWidths}),[t==null?void 0:t.columnWidths])}}const Et={title:"React Aria Components/Table",component:y,excludeStories:["DndTable","makePromise","MyCheckbox"]},me=({initialItems:n})=>{let t=te({initialItems:n});const{dragAndDropHooks:a}=oe({getItems:i=>[...i].filter(l=>!!t.getItem(l)).map(l=>{const r=t.getItem(l);return{"text/plain":r.id,item:JSON.stringify(r)}}),getDropOperation:()=>"move",onReorder:i=>{i.target.dropPosition==="before"?t.moveBefore(i.target.key,i.keys):i.target.dropPosition==="after"&&t.moveAfter(i.target.key,i.keys)},onInsert:async i=>{const l=await Promise.all(i.items.filter(ee).map(async r=>JSON.parse(await r.getText("item"))));i.target.dropPosition==="before"?t.insertBefore(i.target.key,...l):i.target.dropPosition==="after"&&t.insertAfter(i.target.key,...l)},onDragEnd:i=>{i.dropOperation==="move"&&!i.isInternal&&t.remove(...i.keys)},onRootDrop:async i=>{const l=await Promise.all(i.items.filter(ee).map(async r=>JSON.parse(await r.getText("item"))));t.append(...l)}});return e.jsxs(y,{"aria-label":"Reorderable table",dragAndDropHooks:a,children:[e.jsxs(g,{children:[e.jsx(x,{isRowHeader:!0,defaultWidth:"50%",children:"Id"}),e.jsx(x,{children:"Name"})]}),e.jsx(b,{items:t.items,renderEmptyState:({isDropTarget:i})=>e.jsx("span",{style:{color:i?"red":"black"},children:"Drop items here"}),children:i=>e.jsxs(p,{children:[e.jsx(o,{children:i.id}),e.jsx(o,{children:i.name})]})})]})},z=()=>e.jsxs(e.Fragment,{children:[e.jsx(I,{style:{width:300,overflow:"auto"},children:e.jsx(me,{initialItems:[{id:"1",name:"Bob"}]})}),e.jsx(I,{style:{width:300,overflow:"auto"},children:e.jsx(me,{initialItems:[{id:"2",name:"Alex"}]})})]}),Bt=n=>{let t=te({initialItems:[{id:1,name:"Games",date:"6/7/2020",type:"File folder"},{id:2,name:"Program Files",date:"4/7/2021",type:"File folder"},{id:3,name:"bootmgr",date:"11/20/2010",type:"System file"},{id:4,name:"log.txt",date:"1/18/2016",type:"Text Document"}]});return e.jsx(I,{style:{width:400,overflow:"auto"},children:e.jsxs(y,{"aria-label":"Example table",...n,children:[e.jsxs(g,{children:[e.jsx(m,{width:30,minWidth:0,children:e.jsx(T,{slot:"selection"})}),e.jsx(x,{isRowHeader:!0,defaultWidth:"30%",children:"Name"}),e.jsx(x,{children:"Type"}),e.jsx(x,{children:"Date Modified"}),e.jsx(x,{children:"Actions"})]}),e.jsx(b,{items:t.items,children:a=>e.jsxs(p,{children:[e.jsx(o,{children:e.jsx(T,{slot:"selection"})}),e.jsx(o,{children:a.name}),e.jsx(o,{children:a.type}),e.jsx(o,{children:a.date}),e.jsx(o,{children:e.jsxs(xt,{children:[e.jsx(R,{children:"Delete"}),e.jsx(wt,{style:{position:"fixed",zIndex:100,top:0,left:0,bottom:0,right:0,background:"rgba(0, 0, 0, 0.5)",display:"flex",alignItems:"center",justifyContent:"center"},children:e.jsx(jt,{style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:30},children:e.jsx(Tt,{children:({close:i})=>e.jsxs(e.Fragment,{children:[e.jsx(Ct,{slot:"title",children:"Delete item"}),e.jsx("p",{children:"Are you sure?"}),e.jsx(R,{onPress:i,children:"Cancel"}),e.jsx(R,{onPress:()=>{i(),t.remove(a.id)},children:"Delete"})]})})})})]})})]})})]})})},F={render:Bt,args:{selectionMode:"none",selectionBehavior:"toggle",escapeKeyBehavior:"clearSelection"},argTypes:{selectionMode:{control:"radio",options:["none","single","multiple"]},selectionBehavior:{control:"radio",options:["toggle","replace"]},escapeKeyBehavior:{control:"radio",options:["clearSelection","none"]}}};let j=[{name:"Name",id:"name",isRowHeader:!0},{name:"Type",id:"type"},{name:"Date Modified",id:"date"}],de=[{id:0,name:"Games",date:"6/7/2020",type:"File folder"},{id:1,name:"Program Files",date:"4/7/2021",type:"File folder"},{id:2,name:"bootmgr",date:"11/20/2010",type:"System file"},{id:3,name:"log.txt",date:"1/18/20167",type:"Text Document"}];const H=()=>e.jsxs(y,{"aria-label":"Files",children:[e.jsx(g,{columns:j,children:n=>e.jsx(m,{isRowHeader:n.isRowHeader,children:n.name})}),e.jsx(b,{items:de,children:n=>e.jsx(p,{columns:j,id:n.id,children:t=>e.jsx(o,{children:n[t.id]})})})]});let Wt=[{name:"Time",id:"time",isRowHeader:!0},{name:"Monday",id:"monday"},{name:"Tuesday",id:"tuesday"},{name:"Wednesday",id:"wednesday"},{name:"Thursday",id:"thursday"},{name:"Friday",id:"friday"}],_t=[{id:1,time:"08:00 - 09:00",monday:"Math",tuesday:"History",wednesday:"Science",thursday:"English",friday:"Art"},{id:2,time:"09:00 - 10:00",name:"Break",type:"break"},{id:3,time:"10:00 - 11:00",monday:"Math",tuesday:"History",wednesday:"Science",thursday:"English",friday:"Art"},{id:4,time:"11:00 - 12:00",monday:"Math",tuesday:"History",wednesday:"Science",thursday:"English",friday:"Art"},{id:5,time:"12:00 - 13:00",name:"Break",type:"break"},{id:6,time:"13:00 - 14:00",monday:"History",tuesday:"Math",wednesday:"English",thursday:"Science",friday:"Art"}];const L=()=>e.jsxs(y,{"aria-label":"Timetable",children:[e.jsx(g,{columns:Wt,children:n=>e.jsx(m,{isRowHeader:n.isRowHeader,children:n.name})}),e.jsx(b,{items:_t,children:n=>e.jsx(p,{columns:j,children:n.type==="break"?e.jsxs(e.Fragment,{children:[e.jsx(o,{children:n.time}),e.jsx(o,{colSpan:5,children:n.name})]}):e.jsxs(e.Fragment,{children:[e.jsx(o,{children:n.time}),e.jsx(o,{children:n.monday}),e.jsx(o,{children:n.tuesday}),e.jsx(o,{children:n.wednesday}),e.jsx(o,{children:n.thursday}),e.jsx(o,{children:n.friday})]})})})]}),M=()=>e.jsxs(y,{"aria-label":"Table with various colspans",children:[e.jsxs(g,{children:[e.jsx(m,{isRowHeader:!0,children:"Col 1"}),e.jsx(m,{children:"Col 2"}),e.jsx(m,{children:"Col 3"}),e.jsx(m,{children:"Col 4"})]}),e.jsxs(b,{children:[e.jsxs(p,{children:[e.jsx(o,{children:"Cell"}),e.jsx(o,{colSpan:2,children:"Span 2"}),e.jsx(o,{children:"Cell"})]}),e.jsxs(p,{children:[e.jsx(o,{children:"Cell"}),e.jsx(o,{children:"Cell"}),e.jsx(o,{children:"Cell"}),e.jsx(o,{children:"Cell"})]}),e.jsx(p,{children:e.jsx(o,{colSpan:4,children:"Span 4"})}),e.jsxs(p,{children:[e.jsx(o,{children:"Cell"}),e.jsx(o,{children:"Cell"}),e.jsx(o,{children:"Cell"}),e.jsx(o,{children:"Cell"})]}),e.jsxs(p,{children:[e.jsx(o,{colSpan:3,children:"Span 3"}),e.jsx(o,{children:"Cell"})]}),e.jsxs(p,{children:[e.jsx(o,{children:"Cell"}),e.jsx(o,{children:"Cell"}),e.jsx(o,{children:"Cell"}),e.jsx(o,{children:"Cell"})]}),e.jsxs(p,{children:[e.jsx(o,{children:"Cell"}),e.jsx(o,{colSpan:3,children:"Span 3"})]})]})]}),x=n=>e.jsx(m,{...n,children:({startResize:t})=>e.jsxs("div",{style:{display:"flex"},children:[e.jsxs(St,{children:[e.jsx(R,{style:{flex:1,textAlign:"left"},children:n.children}),e.jsx(Rt,{children:e.jsx(It,{className:Dt.menu,onAction:()=>t(),children:e.jsx(Mt,{id:"resize",children:"Resize"})})})]}),e.jsx(kt,{onHoverStart:ie("onHoverStart"),onHoverChange:ie("onHoverChange"),onHoverEnd:ie("onHoverEnd"),children:"↔"})]})});function le(n){let t=te({initialItems:n.initialItems}),{dragAndDropHooks:a}=oe({isDisabled:n.isDisabled,getItems(i){return[...i].filter(l=>!!t.getItem(l)).map(l=>{let r=t.getItem(l);return{"custom-app-type":JSON.stringify(r),"text/plain":r.name}})},acceptedDragTypes:["custom-app-type"],getDropOperation:()=>"move",async onInsert(i){let l=await Promise.all(i.items.filter(ee).map(async r=>JSON.parse(await r.getText("custom-app-type"))));i.target.dropPosition==="before"?t.insertBefore(i.target.key,...l):i.target.dropPosition==="after"&&t.insertAfter(i.target.key,...l)},async onRootDrop(i){let l=await Promise.all(i.items.filter(ee).map(async r=>JSON.parse(await r.getText("custom-app-type"))));t.append(...l)},onReorder(i){i.target.dropPosition==="before"?t.moveBefore(i.target.key,i.keys):i.target.dropPosition==="after"&&t.moveAfter(i.target.key,i.keys)},onDragEnd(i){i.dropOperation==="move"&&!i.isInternal&&t.remove(...i.keys)}});return e.jsxs(y,{"aria-label":n["aria-label"],selectionMode:"multiple",selectedKeys:t.selectedKeys,onSelectionChange:i=>{var l;(l=n.onSelectionChange)==null||l.call(n,i),t.setSelectedKeys(i)},dragAndDropHooks:a,children:[e.jsxs(g,{children:[e.jsx(m,{}),e.jsx(m,{children:e.jsx(T,{slot:"selection"})}),e.jsx(m,{children:"ID"}),e.jsx(m,{isRowHeader:!0,children:"Name"}),e.jsx(m,{children:"Type"})]}),e.jsxs(b,{items:t.items,renderEmptyState:()=>W({isLoading:n.isLoading,tableWidth:200}),children:[e.jsx(Z,{items:t.items,children:i=>e.jsxs(p,{children:[e.jsx(o,{children:e.jsx(R,{slot:"drag",children:"≡"})}),e.jsx(o,{children:e.jsx(T,{slot:"selection"})}),e.jsx(o,{children:i.id}),e.jsx(o,{children:i.name}),e.jsx(o,{children:i.type})]})}),e.jsx(ce,{isLoading:n.isLoading})]})]})}const ut=n=>e.jsx(le,{...n});function Ft(n){return e.jsxs("div",{style:{display:"flex",gap:12,flexWrap:"wrap"},children:[e.jsx(le,{isLoading:n.isLoading,initialItems:[{id:"1",type:"file",name:"Adobe Photoshop"},{id:"2",type:"file",name:"Adobe XD"},{id:"3",type:"folder",name:"Documents"},{id:"4",type:"file",name:"Adobe InDesign"},{id:"5",type:"folder",name:"Utilities"},{id:"6",type:"file",name:"Adobe AfterEffects"}],"aria-label":"First Table",isDisabled:n.isDisabledFirstTable}),e.jsx(le,{isLoading:n.isLoading,initialItems:[{id:"7",type:"folder",name:"Pictures"},{id:"8",type:"file",name:"Adobe Fresco"},{id:"9",type:"folder",name:"Apps"},{id:"10",type:"file",name:"Adobe Illustrator"},{id:"11",type:"file",name:"Adobe Lightroom"},{id:"12",type:"file",name:"Adobe Dreamweaver"}],"aria-label":"Second Table",isDisabled:n.isDisabledSecondTable})]})}const S=n=>e.jsx(Ft,{...n});S.args={isDisabledFirstTable:!1,isDisabledSecondTable:!1,isLoading:!1};const T=({children:n,...t})=>e.jsx(vt,{...t,children:({isIndeterminate:a})=>e.jsxs(e.Fragment,{children:[e.jsx("div",{className:"checkbox",children:e.jsx("svg",{viewBox:"0 0 18 18","aria-hidden":"true",children:a?e.jsx("rect",{x:1,y:7.5,width:15,height:3}):e.jsx("polyline",{points:"1 9 7 14 15 4"})})}),n]})}),ce=n=>{let{tableWidth:t=400,...a}=n;return e.jsx(Ht,{style:{height:30,width:t},...a,children:e.jsx(mt,{style:{height:20,position:"unset"}})})};function G(n){let{rows:t,children:a,isLoading:i,onLoadMore:l,tableWidth:r,...s}=n;return e.jsxs(b,{...s,children:[e.jsx(Z,{items:t,children:a}),e.jsx(ce,{tableWidth:r,isLoading:i,onLoadMore:l})]})}const At=n=>e.jsxs(y,{"aria-label":"Files",children:[e.jsx(g,{columns:j,children:t=>e.jsx(m,{isRowHeader:t.isRowHeader,children:t.name})}),e.jsx(G,{rows:de,isLoading:n.isLoadingMore,children:t=>e.jsx(p,{columns:j,children:a=>e.jsx(o,{children:t[a.id]})})})]}),A={render:At,args:{isLoadingMore:!1},name:"Table loading, table body wrapper with collection"};function $t(n){return e.jsxs(e.Fragment,{children:[e.jsx(p,{...n}),n.shouldRenderLoader&&e.jsx(ce,{isLoading:n.isLoadingMore})]})}const Nt=n=>e.jsxs(y,{"aria-label":"Files",children:[e.jsx(g,{columns:j,children:t=>e.jsx(m,{isRowHeader:t.isRowHeader,children:t.name})}),e.jsx(b,{items:de,dependencies:[n.isLoadingMore],children:t=>e.jsx($t,{columns:j,shouldRenderLoader:t.id===4,isLoadingMore:n.isLoadingMore,children:a=>e.jsx(o,{children:t[a.id]})})})]}),$={render:Nt,args:{isLoadingMore:!1},name:"Table loading, row renderer wrapper and dep array"};function W({isLoading:n,tableWidth:t=400}){let a=n?e.jsx(mt,{style:{height:20,width:20,transform:"translate(-50%, -50%)"}}):"No results found";return e.jsx("div",{style:{height:30,position:"sticky",top:0,left:0,width:t},children:a})}const Vt=n=>{let{isLoading:t}=n;return e.jsxs(y,{"aria-label":"Files",selectionMode:"multiple",children:[e.jsxs(g,{columns:j,children:[e.jsx(m,{children:e.jsx(T,{slot:"selection"})}),e.jsx(Z,{items:j,children:a=>e.jsx(m,{isRowHeader:a.isRowHeader,children:a.name})})]}),e.jsx(b,{renderEmptyState:()=>W({isLoading:t}),children:e.jsx(Z,{items:[],children:a=>e.jsx(p,{columns:j,children:i=>e.jsx(o,{children:a[i.id]})})})})]})},N={render:Vt,args:{isLoading:!1},name:"Empty/Loading Table rendered with TableLoadingIndicator collection element"},Ot=n=>{let t=se({async load({signal:a,cursor:i}){i&&(i=i.replace(/^http:\/\//i,"https://")),await new Promise(s=>setTimeout(s,n.delay));let r=await(await fetch(i||"https://swapi.py4e.com/api/people/?search=",{signal:a})).json();return{items:r.results,cursor:r.next}}});return e.jsx(I,{style:{height:150,width:400,overflow:"auto"},children:e.jsxs(y,{"aria-label":"Load more table",children:[e.jsxs(g,{children:[e.jsx(m,{id:"name",isRowHeader:!0,style:{position:"sticky",top:0,backgroundColor:"lightgray"},children:"Name"}),e.jsx(m,{id:"height",style:{position:"sticky",top:0,backgroundColor:"lightgray"},children:"Height"}),e.jsx(m,{id:"mass",style:{position:"sticky",top:0,backgroundColor:"lightgray"},children:"Mass"}),e.jsx(m,{id:"birth_year",style:{position:"sticky",top:0,backgroundColor:"lightgray"},children:"Birth Year"})]}),e.jsx(G,{tableWidth:400,renderEmptyState:()=>W({isLoading:t.loadingState==="loading",tableWidth:400}),isLoading:t.loadingState==="loadingMore",onLoadMore:t.loadMore,rows:t.items,children:a=>e.jsxs(p,{id:a.name,style:{width:"inherit",height:"inherit"},children:[e.jsx(o,{children:a.name}),e.jsx(o,{children:a.height}),e.jsx(o,{children:a.mass}),e.jsx(o,{children:a.birth_year})]})})]})})},V={render:Ot,name:"onLoadMore table",args:{delay:50}},D=()=>{let n=[];for(let i=0;i<1e3;i++)n.push({id:i,foo:`Foo ${i}`,bar:`Bar ${i}`,baz:`Baz ${i}`});let t=te({initialItems:n}),{dragAndDropHooks:a}=oe({getItems:i=>[...i].filter(l=>!!t.getItem(l)).map(l=>({"text/plain":t.getItem(l).foo})),onReorder(i){i.target.dropPosition==="before"?t.moveBefore(i.target.key,i.keys):i.target.dropPosition==="after"&&t.moveAfter(i.target.key,i.keys)},renderDropIndicator(i){return e.jsx(zt,{target:i,style:({isDropTarget:l})=>({width:"100%",height:"100%",background:l?"blue":"transparent"})})}});return e.jsx(U,{layout:J,layoutOptions:{rowHeight:25,headingHeight:25},children:e.jsxs(y,{"aria-label":"virtualized table",selectionMode:"multiple",dragAndDropHooks:a,style:{height:400,width:400,overflow:"auto",scrollPaddingTop:25},children:[e.jsxs(g,{style:{background:"var(--spectrum-gray-100)",width:"100%",height:"100%"},children:[e.jsx(m,{width:30,minWidth:0}),e.jsx(m,{width:30,minWidth:0,children:e.jsx(T,{slot:"selection"})}),e.jsx(m,{isRowHeader:!0,children:e.jsx("strong",{children:"Foo"})}),e.jsx(m,{children:e.jsx("strong",{children:"Bar"})}),e.jsx(m,{children:e.jsx("strong",{children:"Baz"})})]}),e.jsx(b,{items:t.items,children:i=>e.jsxs(p,{style:{width:"inherit",height:"inherit"},children:[e.jsx(o,{children:e.jsx(R,{slot:"drag",children:"≡"})}),e.jsx(o,{children:e.jsx(T,{slot:"selection"})}),e.jsx(o,{children:i.foo}),e.jsx(o,{children:i.bar}),e.jsx(o,{children:i.baz})]})})]})})},P=()=>{let n=[];for(let t=0;t<1e3;t++)n.push({id:t,foo:`Foo ${t}`,bar:`Bar ${t}`,baz:`Baz ${t}`});return e.jsx(I,{style:{height:400,width:400,overflow:"auto",scrollPaddingTop:25},children:e.jsx(U,{layout:J,layoutOptions:{rowHeight:25,headingHeight:25},children:e.jsxs(y,{"aria-label":"virtualized table",children:[e.jsxs(g,{style:{background:"var(--spectrum-gray-100)",width:"100%",height:"100%"},children:[e.jsx(x,{isRowHeader:!0,children:"Foo"}),e.jsx(x,{children:"Bar"}),e.jsx(x,{children:"Baz"})]}),e.jsx(b,{items:n,children:t=>e.jsxs(p,{style:{width:"inherit",height:"inherit"},children:[e.jsx(o,{children:t.foo}),e.jsx(o,{children:t.bar}),e.jsx(o,{children:t.baz})]})})]})})})};function Kt(n){let t=[{foo:"Foo 1",bar:"Bar 1",baz:"Baz 1"},{foo:"Foo 2",bar:"Bar 2",baz:"Baz 2"},{foo:"Foo 3",bar:"Bar 3",baz:"Baz 3"},{foo:"Foo 4",bar:"Bar 4",baz:"Baz 4"}];return e.jsx(I,{style:{height:400,width:400,overflow:"auto",scrollPaddingTop:25},children:e.jsx(U,{layout:J,layoutOptions:{rowHeight:25,headingHeight:25},children:e.jsxs(y,{"aria-label":"virtualized table",children:[e.jsxs(g,{style:{background:"var(--spectrum-gray-100)",width:"100%",height:"100%"},children:[e.jsx(x,{isRowHeader:!0,children:"Foo"}),e.jsx(x,{children:"Bar"}),e.jsx(x,{children:"Baz"})]}),e.jsx(G,{isLoading:n.isLoading&&n.showRows,renderEmptyState:()=>W({isLoading:!n.showRows&&n.isLoading}),rows:n.showRows?t:[],children:a=>e.jsxs(p,{id:a.foo,style:{width:"inherit",height:"inherit"},children:[e.jsx(o,{children:a.foo}),e.jsx(o,{children:a.bar}),e.jsx(o,{children:a.baz})]})})]})})})}const O={render:Kt,args:{isLoading:!1,showRows:!1},name:"Virtualized Table With Empty State"},Yt=n=>{let t=se({async load({signal:a,cursor:i}){i&&(i=i.replace(/^http:\/\//i,"https://")),await new Promise(s=>setTimeout(s,n.delay));let r=await(await fetch(i||"https://swapi.py4e.com/api/people/?search=",{signal:a})).json();return{items:r.results,cursor:r.next}}});return e.jsx(U,{layout:J,layoutOptions:{rowHeight:25,headingHeight:25,loaderHeight:30},children:e.jsxs(y,{"aria-label":"Load more table virtualized",style:{height:150,width:400,overflow:"auto"},children:[e.jsxs(g,{style:{background:"var(--spectrum-gray-100)",width:"100%",height:"100%"},children:[e.jsx(m,{id:"name",isRowHeader:!0,children:"Name"}),e.jsx(m,{id:"height",children:"Height"}),e.jsx(m,{id:"mass",children:"Mass"}),e.jsx(m,{id:"birth_year",children:"Birth Year"})]}),e.jsx(G,{renderEmptyState:()=>W({isLoading:t.loadingState==="loading"}),isLoading:t.loadingState==="loadingMore",onLoadMore:t.loadMore,rows:t.items,children:a=>e.jsxs(p,{id:a.name,style:{width:"inherit",height:"inherit"},children:[e.jsx(o,{children:a.name}),e.jsx(o,{children:a.height}),e.jsx(o,{children:a.mass}),e.jsx(o,{children:a.birth_year})]})})]})})},K={render:Yt,name:"Virtualized Table with async loading",args:{delay:50}},qt=n=>{let t=se({async load({signal:a,cursor:i}){i&&(i=i.replace(/^http:\/\//i,"https://")),await new Promise(s=>setTimeout(s,n.delay));let r=await(await fetch(i||"https://swapi.py4e.com/api/people/?search=",{signal:a})).json();return{items:r.results,cursor:r.next}}});return e.jsx(I,{style:{height:150,width:400,overflow:"auto"},children:e.jsx(U,{layout:J,layoutOptions:{rowHeight:25,headingHeight:25,loaderHeight:30},children:e.jsxs(y,{"aria-label":"Load more table virtualized",children:[e.jsxs(g,{style:{background:"var(--spectrum-gray-100)",width:"100%",height:"100%"},children:[e.jsx(m,{id:"name",isRowHeader:!0,children:"Name"}),e.jsx(m,{id:"height",children:"Height"}),e.jsx(m,{id:"mass",children:"Mass"}),e.jsx(m,{id:"birth_year",children:"Birth Year"})]}),e.jsx(G,{renderEmptyState:()=>W({isLoading:t.loadingState==="loading"}),isLoading:t.loadingState==="loadingMore",onLoadMore:t.loadMore,rows:t.items,children:a=>e.jsxs(p,{id:a.name,style:{width:"inherit",height:"inherit"},children:[e.jsx(o,{children:a.name}),e.jsx(o,{children:a.height}),e.jsx(o,{children:a.mass}),e.jsx(o,{children:a.birth_year})]})})]})})})},Y={render:qt,name:"Virtualized Table with async loading, with wrapper around Virtualizer",args:{delay:50},parameters:{description:{data:"This table has a ResizableTableContainer wrapper around the Virtualizer. The table itself doesnt have any resizablity, this is simply to test that it still loads/scrolls in this configuration."}}},ue=[{id:0,mission_name:"FalconSat",launch_year:2006},{id:1,mission_name:"DemoSat",launch_year:2007},{id:2,mission_name:"Trailblazer",launch_year:2008},{id:3,mission_name:"RatSat",launch_year:2009}];function ne(n){return new Promise(t=>setTimeout(()=>t(n),1e3))}function Ut({reactTransition:n=!1}){let[t,a]=B.useState(()=>ne(ue.slice(0,2))),[i,l]=re.useTransition();return e.jsxs("div",{children:[e.jsxs(y,{"aria-label":"Suspense table",children:[e.jsxs(g,{children:[e.jsx(m,{isRowHeader:!0,children:"Name"}),e.jsx(m,{children:"Year"})]}),e.jsx(b,{children:e.jsx(B.Suspense,{fallback:e.jsx(p,{children:e.jsx(o,{colSpan:2,children:"Loading..."})}),children:e.jsx(Jt,{promise:t})})})]}),e.jsx("button",{onClick:()=>{let r=()=>{a(ne(ue))};n?l(r):r()},children:i?"Loading":"Load more"})]})}function Jt({promise:n}){return re.use(n).map(a=>e.jsxs(p,{children:[e.jsx(o,{children:a.mission_name}),e.jsx(o,{children:a.launch_year})]},a.id))}const q={render:re.use!=null?n=>e.jsx(Ut,{...n}):()=>e.jsx(e.Fragment,{children:"'This story requires React 19.'"}),args:{reactTransition:!1},parameters:{description:{data:"Expected behavior: With reactTransition=false, rows should be replaced by loading indicator when pressing button. With reactTransition=true, existing rows should remain and loading should appear inside the button."}}};let Gt=[{id:25,name:"Web Development",date:"7/10/2023",type:"File folder"},{id:26,name:"drivers",date:"2/2/2022",type:"System file"},{id:27,name:"debug.txt",date:"12/5/2024",type:"Text Document"},{id:28,name:"Marketing Plan.pptx",date:"3/15/2025",type:"PowerPoint file"},{id:29,name:"Contract_v3.pdf",date:"1/2/2025",type:"PDF Document"},{id:30,name:"Movies",date:"5/20/2024",type:"File folder"},{id:31,name:"User Manual.docx",date:"9/1/2024",type:"Word Document"},{id:32,name:"Sales Data_Q1.xlsx",date:"4/10/2025",type:"Excel file"},{id:33,name:"archive_old.rar",date:"6/1/2023",type:"RAR archive"},{id:34,name:"logo.svg",date:"11/22/2024",type:"SVG image"},{id:35,name:"main.py",date:"10/1/2024",type:"Python file"},{id:36,name:"base.html",date:"8/18/2024",type:"HTML file"},{id:37,name:"Configurations",date:"4/5/2024",type:"File folder"},{id:38,name:"kernel32.dll",date:"9/10/2018",type:"System file"},{id:39,name:"security_log.txt",date:"3/28/2025",type:"Text Document"},{id:40,name:"Project Proposal v2.pptx",date:"1/15/2025",type:"PowerPoint file"},{id:41,name:"NDA_Signed.pdf",date:"12/20/2024",type:"PDF Document"},{id:42,name:"Downloads",date:"7/1/2024",type:"File folder"},{id:43,name:"Meeting Minutes.docx",date:"4/12/2025",type:"Word Document"},{id:44,name:"Financial Report_FY24.xlsx",date:"3/5/2025",type:"Excel file"},{id:45,name:"data_backup_v1.tar.gz",date:"11/8/2024",type:"GZIP archive"},{id:46,name:"icon.ico",date:"6/25/2024",type:"ICO file"},{id:47,name:"app.config",date:"9/30/2024",type:"Configuration file"},{id:48,name:"Templates",date:"2/10/2025",type:"File folder"}],Xt=[{id:100,name:"Assets",date:"8/15/2024",type:"File folder"},{id:101,name:"drivers64",date:"3/3/2023",type:"System file"},{id:102,name:"install.log",date:"1/8/2025",type:"Text Document"},{id:103,name:"Product Demo.pptx",date:"4/20/2025",type:"PowerPoint file"},{id:104,name:"Terms_of_Service.pdf",date:"2/5/2025",type:"PDF Document"},{id:105,name:"Animations",date:"6/25/2024",type:"File folder"},{id:106,name:"Release Notes.docx",date:"10/1/2024",type:"Word Document"},{id:107,name:"Financial Projections.xlsx",date:"5/12/2025",type:"Excel file"},{id:108,name:"backup_2023.tar",date:"7/1/2024",type:"TAR archive"},{id:109,name:"thumbnail.jpg",date:"12/1/2024",type:"JPEG image"},{id:110,name:"api_client.py",date:"11/15/2024",type:"Python file"},{id:111,name:"index.html",date:"9/28/2024",type:"HTML file"},{id:112,name:"Resources",date:"5/5/2024",type:"File folder"},{id:113,name:"msvcr100.dll",date:"10/10/2019",type:"System file"},{id:114,name:"system_events.txt",date:"4/1/2025",type:"Text Document"},{id:115,name:"Training Presentation.pptx",date:"2/20/2025",type:"PowerPoint file"},{id:116,name:"Privacy_Policy.pdf",date:"1/10/2025",type:"PDF Document"},{id:117,name:"Desktop",date:"8/1/2024",type:"File folder"},{id:118,name:"Meeting Agenda.docx",date:"5/15/2025",type:"Word Document"},{id:119,name:"Budget_Forecast.xlsx",date:"4/15/2025",type:"Excel file"},{id:120,name:"code_backup.7z",date:"12/1/2024",type:"7Z archive"},{id:121,name:"icon_large.ico",date:"7/1/2024",type:"ICO file"},{id:122,name:"settings.ini",date:"10/5/2024",type:"Configuration file"},{id:123,name:"Project Docs",date:"3/1/2025",type:"File folder"},{id:124,name:"winload.exe",date:"11/1/2010",type:"System file"},{id:125,name:"application.log",date:"6/1/2025",type:"Text Document"},{id:126,name:"Client Presentation.pptx",date:"3/1/2025",type:"PowerPoint file"},{id:127,name:"EULA.pdf",date:"2/15/2025",type:"PDF Document"},{id:128,name:"Temporary",date:"9/1/2024",type:"File folder"},{id:129,name:"Action Items.docx",date:"6/1/2025",type:"Word Document"},{id:130,name:"Revenue_Report.xlsx",date:"5/20/2025",type:"Excel file"},{id:131,name:"data_dump.sql",date:"1/1/2025",type:"SQL Dump"},{id:132,name:"image_preview.bmp",date:"8/20/2024",type:"Bitmap image"},{id:133,name:"server.conf",date:"11/20/2024",type:"Configuration file"},{id:134,name:"Documentation",date:"4/1/2025",type:"File folder"},{id:135,name:"hal.dll",date:"12/25/2007",type:"System file"},{id:136,name:"access.log",date:"7/1/2025",type:"Text Document"},{id:137,name:"Strategy Presentation.pptx",date:"4/1/2025",type:"PowerPoint file"},{id:138,name:"Service Agreement.pdf",date:"3/1/2025",type:"PDF Document"},{id:139,name:"Recycle Bin",date:"1/1/2000",type:"System folder"}];const pe=[{id:"name",name:"Name",isRowHeader:!0,allowsSorting:!0},{id:"type",name:"Type",allowsSorting:!0},{id:"date",name:"Date Modified",allowsSorting:!0}],E=()=>{const[n,t]=B.useState(!0),a=n?Xt:Gt;return e.jsxs("div",{children:[e.jsx(R,{onPress:()=>B.startTransition(()=>{t(i=>!i)}),children:"Toggle data using useState + startTransition"}),e.jsxs(y,{"aria-label":"test",children:[e.jsx(g,{columns:pe,children:i=>e.jsx(m,{...i,children:i.name})}),e.jsx(b,{items:a,children:i=>e.jsx(p,{id:i.id,columns:pe,children:l=>e.jsx(o,{children:i[l.id]})})})]})]})};z.__docgenInfo={description:"",methods:[],displayName:"ReorderableTableExample"};H.__docgenInfo={description:"",methods:[],displayName:"TableDynamicExample"};L.__docgenInfo={description:"",methods:[],displayName:"TableCellColSpanExample"};M.__docgenInfo={description:"",methods:[],displayName:"TableCellColSpanWithVariousSpansExample"};ut.__docgenInfo={description:"",methods:[],displayName:"DndTable"};S.__docgenInfo={description:"",methods:[],displayName:"DndTableExample"};T.__docgenInfo={description:"",methods:[],displayName:"MyCheckbox",props:{validationBehavior:{required:!1,tsType:{name:"union",raw:"'native' | 'aria'",elements:[{name:"literal",value:"'native'"},{name:"literal",value:"'aria'"}]},description:`Whether to use native HTML form validation to prevent form submission
when the value is missing or invalid, or mark the field as required
or invalid via ARIA.
@default 'native'`},className:{required:!1,tsType:{name:"union",raw:"string | ((values: T & {defaultClassName: string | undefined}) => string)",elements:[{name:"string"},{name:"unknown"}]},description:"The CSS [className](https://developer.mozilla.org/en-US/docs/Web/API/Element/className) for the element. A function may be provided to compute the class based on component state."},style:{required:!1,tsType:{name:"union",raw:"CSSProperties | ((values: T & {defaultStyle: CSSProperties}) => CSSProperties | undefined)",elements:[{name:"CSSProperties"},{name:"unknown"}]},description:"The inline [style](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style) for the element. A function may be provided to compute the style based on component state."},children:{required:!1,tsType:{name:"union",raw:"ReactNode | ((values: T & {defaultChildren: ReactNode | undefined}) => ReactNode)",elements:[{name:"ReactNode"},{name:"unknown"}]},description:"The children of the component. A function may be provided to alter the children based on component state."},slot:{required:!1,tsType:{name:"union",raw:"string | null",elements:[{name:"string"},{name:"null"}]},description:"A slot name for the component. Slots allow the component to receive props from a parent component.\nAn explicit `null` value indicates that the local props completely override all props received from a parent."},inputRef:{required:!1,tsType:{name:"RefObject",elements:[{name:"union",raw:"HTMLInputElement | null",elements:[{name:"HTMLInputElement"},{name:"null"}]}],raw:"RefObject<HTMLInputElement | null>"},description:"A ref for the HTML input element."}},composes:["Omit","HoverEvents"]};D.__docgenInfo={description:"",methods:[],displayName:"VirtualizedTable"};P.__docgenInfo={description:"",methods:[],displayName:"VirtualizedTableWithResizing"};E.__docgenInfo={description:"",methods:[],displayName:"TableWithReactTransition"};var ye,ge,fe;z.parameters={...z.parameters,docs:{...(ye=z.parameters)==null?void 0:ye.docs,source:{originalSource:`() => <>
    <ResizableTableContainer style={{
    width: 300,
    overflow: 'auto'
  }}>
      <ReorderableTable initialItems={[{
      id: '1',
      name: 'Bob'
    }]} />
    </ResizableTableContainer>
    <ResizableTableContainer style={{
    width: 300,
    overflow: 'auto'
  }}>
      <ReorderableTable initialItems={[{
      id: '2',
      name: 'Alex'
    }]} />
    </ResizableTableContainer>
  </>`,...(fe=(ge=z.parameters)==null?void 0:ge.docs)==null?void 0:fe.source}}};var be,xe,we;F.parameters={...F.parameters,docs:{...(be=F.parameters)==null?void 0:be.docs,source:{originalSource:`{
  render: TableExample,
  args: {
    selectionMode: 'none',
    selectionBehavior: 'toggle',
    escapeKeyBehavior: 'clearSelection'
  },
  argTypes: {
    selectionMode: {
      control: 'radio',
      options: ['none', 'single', 'multiple']
    },
    selectionBehavior: {
      control: 'radio',
      options: ['toggle', 'replace']
    },
    escapeKeyBehavior: {
      control: 'radio',
      options: ['clearSelection', 'none']
    }
  }
}`,...(we=(xe=F.parameters)==null?void 0:xe.docs)==null?void 0:we.source}}};var je,Te,Ce;H.parameters={...H.parameters,docs:{...(je=H.parameters)==null?void 0:je.docs,source:{originalSource:`() => {
  return <Table aria-label="Files">
      <TableHeader columns={columns}>
        {column => <Column isRowHeader={column.isRowHeader}>{column.name}</Column>}
      </TableHeader>
      <TableBody items={rows}>
        {item => <Row columns={columns} id={item.id}>
            {column => {
          return <Cell>{item[column.id]}</Cell>;
        }}
          </Row>}
      </TableBody>
    </Table>;
}`,...(Ce=(Te=H.parameters)==null?void 0:Te.docs)==null?void 0:Ce.source}}};var ve,Se,Re;L.parameters={...L.parameters,docs:{...(ve=L.parameters)==null?void 0:ve.docs,source:{originalSource:`() => {
  return <Table aria-label="Timetable">
      <TableHeader columns={timeTableColumns}>
        {column => <Column isRowHeader={column.isRowHeader}>{column.name}</Column>}
      </TableHeader>
      <TableBody items={timeTableRows}>
        {item => <Row columns={columns}>
            {item.type === 'break' ? <>
                <Cell>{item.time}</Cell>
                <Cell colSpan={5}>{item.name}</Cell>
              </> : <>
                <Cell>{item.time}</Cell>
                <Cell>{item.monday}</Cell>
                <Cell>{item.tuesday}</Cell>
                <Cell>{item.wednesday}</Cell>
                <Cell>{item.thursday}</Cell>
                <Cell>{item.friday}</Cell>
              </>}
          </Row>}
      </TableBody>
    </Table>;
}`,...(Re=(Se=L.parameters)==null?void 0:Se.docs)==null?void 0:Re.source}}};var Ie,ke,ze;M.parameters={...M.parameters,docs:{...(Ie=M.parameters)==null?void 0:Ie.docs,source:{originalSource:`() => {
  return <Table aria-label="Table with various colspans">
      <TableHeader>
        <Column isRowHeader>Col 1</Column>
        <Column>Col 2</Column>
        <Column>Col 3</Column>
        <Column>Col 4</Column>
      </TableHeader>
      <TableBody>
        <Row>
          <Cell>Cell</Cell>
          <Cell colSpan={2}>Span 2</Cell>
          <Cell>Cell</Cell>
        </Row>
        <Row>
          <Cell>Cell</Cell>
          <Cell>Cell</Cell>
          <Cell>Cell</Cell>
          <Cell>Cell</Cell>
        </Row>
        <Row>
          <Cell colSpan={4}>Span 4</Cell>
        </Row>
        <Row>
          <Cell>Cell</Cell>
          <Cell>Cell</Cell>
          <Cell>Cell</Cell>
          <Cell>Cell</Cell>
        </Row>
        <Row>
          <Cell colSpan={3}>Span 3</Cell>
          <Cell>Cell</Cell>
        </Row>
        <Row>
          <Cell>Cell</Cell>
          <Cell>Cell</Cell>
          <Cell>Cell</Cell>
          <Cell>Cell</Cell>
        </Row>
        <Row>
          <Cell>Cell</Cell>
          <Cell colSpan={3}>Span 3</Cell>
        </Row>
      </TableBody>
    </Table>;
}`,...(ze=(ke=M.parameters)==null?void 0:ke.docs)==null?void 0:ze.source}}};var He,Le,Me;S.parameters={...S.parameters,docs:{...(He=S.parameters)==null?void 0:He.docs,source:{originalSource:`props => {
  return <DndTableExampleRender {...props} />;
}`,...(Me=(Le=S.parameters)==null?void 0:Le.docs)==null?void 0:Me.source}}};var De,Pe,Ee;A.parameters={...A.parameters,docs:{...(De=A.parameters)==null?void 0:De.docs,source:{originalSource:`{
  render: TableLoadingBodyWrapper,
  args: {
    isLoadingMore: false
  },
  name: 'Table loading, table body wrapper with collection'
}`,...(Ee=(Pe=A.parameters)==null?void 0:Pe.docs)==null?void 0:Ee.source}}};var Be,We,_e;$.parameters={...$.parameters,docs:{...(Be=$.parameters)==null?void 0:Be.docs,source:{originalSource:`{
  render: TableLoadingRowRenderWrapper,
  args: {
    isLoadingMore: false
  },
  name: 'Table loading, row renderer wrapper and dep array'
}`,...(_e=(We=$.parameters)==null?void 0:We.docs)==null?void 0:_e.source}}};var Fe,Ae,$e;N.parameters={...N.parameters,docs:{...(Fe=N.parameters)==null?void 0:Fe.docs,source:{originalSource:`{
  render: RenderEmptyState,
  args: {
    isLoading: false
  },
  name: 'Empty/Loading Table rendered with TableLoadingIndicator collection element'
}`,...($e=(Ae=N.parameters)==null?void 0:Ae.docs)==null?void 0:$e.source}}};var Ne,Ve,Oe;V.parameters={...V.parameters,docs:{...(Ne=V.parameters)==null?void 0:Ne.docs,source:{originalSource:`{
  render: OnLoadMoreTable,
  name: 'onLoadMore table',
  args: {
    delay: 50
  }
}`,...(Oe=(Ve=V.parameters)==null?void 0:Ve.docs)==null?void 0:Oe.source}}};var Ke,Ye,qe;D.parameters={...D.parameters,docs:{...(Ke=D.parameters)==null?void 0:Ke.docs,source:{originalSource:`() => {
  let items: {
    id: number;
    foo: string;
    bar: string;
    baz: string;
  }[] = [];
  for (let i = 0; i < 1000; i++) {
    items.push({
      id: i,
      foo: \`Foo \${i}\`,
      bar: \`Bar \${i}\`,
      baz: \`Baz \${i}\`
    });
  }
  let list = useListData({
    initialItems: items
  });
  let {
    dragAndDropHooks
  } = useDragAndDrop({
    getItems: keys => {
      return [...keys].filter(k => !!list.getItem(k)).map(key => ({
        'text/plain': list.getItem(key)!.foo
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
  return <Virtualizer layout={TableLayout} layoutOptions={{
    rowHeight: 25,
    headingHeight: 25
  }}>
      <Table aria-label="virtualized table" selectionMode="multiple" dragAndDropHooks={dragAndDropHooks} style={{
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
          <Column width={30} minWidth={0} />
          <Column width={30} minWidth={0}><MyCheckbox slot="selection" /></Column>
          <Column isRowHeader><strong>Foo</strong></Column>
          <Column><strong>Bar</strong></Column>
          <Column><strong>Baz</strong></Column>
        </TableHeader>
        <TableBody items={list.items}>
          {item => <Row style={{
          width: 'inherit',
          height: 'inherit'
        }}>
              <Cell><Button slot="drag">≡</Button></Cell>
              <Cell><MyCheckbox slot="selection" /></Cell>
              <Cell>{item.foo}</Cell>
              <Cell>{item.bar}</Cell>
              <Cell>{item.baz}</Cell>
            </Row>}
        </TableBody>
      </Table>
    </Virtualizer>;
}`,...(qe=(Ye=D.parameters)==null?void 0:Ye.docs)==null?void 0:qe.source}}};var Ue,Je,Ge;P.parameters={...P.parameters,docs:{...(Ue=P.parameters)==null?void 0:Ue.docs,source:{originalSource:`() => {
  let items: {
    id: number;
    foo: string;
    bar: string;
    baz: string;
  }[] = [];
  for (let i = 0; i < 1000; i++) {
    items.push({
      id: i,
      foo: \`Foo \${i}\`,
      bar: \`Bar \${i}\`,
      baz: \`Baz \${i}\`
    });
  }
  return <ResizableTableContainer style={{
    height: 400,
    width: 400,
    overflow: 'auto',
    scrollPaddingTop: 25
  }}>
      <Virtualizer layout={TableLayout} layoutOptions={{
      rowHeight: 25,
      headingHeight: 25
    }}>
        <Table aria-label="virtualized table">
          <TableHeader style={{
          background: 'var(--spectrum-gray-100)',
          width: '100%',
          height: '100%'
        }}>
            <MyColumn isRowHeader>Foo</MyColumn>
            <MyColumn>Bar</MyColumn>
            <MyColumn>Baz</MyColumn>
          </TableHeader>
          <TableBody items={items}>
            {item => <Row style={{
            width: 'inherit',
            height: 'inherit'
          }}>
                <Cell>{item.foo}</Cell>
                <Cell>{item.bar}</Cell>
                <Cell>{item.baz}</Cell>
              </Row>}
          </TableBody>
        </Table>
      </Virtualizer>
    </ResizableTableContainer>;
}`,...(Ge=(Je=P.parameters)==null?void 0:Je.docs)==null?void 0:Ge.source}}};var Xe,Qe,Ze;O.parameters={...O.parameters,docs:{...(Xe=O.parameters)==null?void 0:Xe.docs,source:{originalSource:`{
  render: VirtualizedTableWithEmptyState,
  args: {
    isLoading: false,
    showRows: false
  },
  name: 'Virtualized Table With Empty State'
}`,...(Ze=(Qe=O.parameters)==null?void 0:Qe.docs)==null?void 0:Ze.source}}};var et,tt,it;K.parameters={...K.parameters,docs:{...(et=K.parameters)==null?void 0:et.docs,source:{originalSource:`{
  render: OnLoadMoreTableVirtualized,
  name: 'Virtualized Table with async loading',
  args: {
    delay: 50
  }
}`,...(it=(tt=K.parameters)==null?void 0:tt.docs)==null?void 0:it.source}}};var at,lt,nt;Y.parameters={...Y.parameters,docs:{...(at=Y.parameters)==null?void 0:at.docs,source:{originalSource:`{
  render: OnLoadMoreTableVirtualizedResizeWrapper,
  name: 'Virtualized Table with async loading, with wrapper around Virtualizer',
  args: {
    delay: 50
  },
  parameters: {
    description: {
      data: 'This table has a ResizableTableContainer wrapper around the Virtualizer. The table itself doesnt have any resizablity, this is simply to test that it still loads/scrolls in this configuration.'
    }
  }
}`,...(nt=(lt=Y.parameters)==null?void 0:lt.docs)==null?void 0:nt.source}}};var rt,st,ot;q.parameters={...q.parameters,docs:{...(rt=q.parameters)==null?void 0:rt.docs,source:{originalSource:`{
  render: React.use != null ? args => <TableSuspense {...args} /> : () => <>'This story requires React 19.'</>,
  args: {
    reactTransition: false
  },
  parameters: {
    description: {
      data: 'Expected behavior: With reactTransition=false, rows should be replaced by loading indicator when pressing button. With reactTransition=true, existing rows should remain and loading should appear inside the button.'
    }
  }
}`,...(ot=(st=q.parameters)==null?void 0:st.docs)==null?void 0:ot.source}}};var dt,ct,ht;E.parameters={...E.parameters,docs:{...(dt=E.parameters)==null?void 0:dt.docs,source:{originalSource:`() => {
  const [show, setShow] = useState(true);
  const items = show ? rows2 : rows1;
  return <div>
      <Button onPress={() => startTransition(() => {
      setShow(s => !s);
    })}>
        Toggle data using useState + startTransition
      </Button>
      <Table aria-label="test">
        <TableHeader columns={columns1}>
          {column => <Column {...column}>{column.name}</Column>}
        </TableHeader>
        <TableBody items={items}>
          {(row: any) => <Row id={row.id} columns={columns1}>
              {/* @ts-ignore */}
              {column => <Cell>{row[column.id]}</Cell>}
            </Row>}
        </TableBody>
      </Table>
    </div>;
}`,...(ht=(ct=E.parameters)==null?void 0:ct.docs)==null?void 0:ht.source}}};const Qt=["ReorderableTableExample","TableExampleStory","TableDynamicExample","TableCellColSpanExample","TableCellColSpanWithVariousSpansExample","DndTable","DndTableExample","MyCheckbox","TableLoadingBodyWrapperStory","TableLoadingRowRenderWrapperStory","RenderEmptyStateStory","OnLoadMoreTableStory","VirtualizedTable","VirtualizedTableWithResizing","VirtualizedTableWithEmptyStateStory","OnLoadMoreTableStoryVirtualized","OnLoadMoreTableVirtualizedResizeWrapperStory","makePromise","TableWithSuspense","TableWithReactTransition"],di=Object.freeze(Object.defineProperty({__proto__:null,DndTable:ut,DndTableExample:S,MyCheckbox:T,OnLoadMoreTableStory:V,OnLoadMoreTableStoryVirtualized:K,OnLoadMoreTableVirtualizedResizeWrapperStory:Y,RenderEmptyStateStory:N,ReorderableTableExample:z,TableCellColSpanExample:L,TableCellColSpanWithVariousSpansExample:M,TableDynamicExample:H,TableExampleStory:F,TableLoadingBodyWrapperStory:A,TableLoadingRowRenderWrapperStory:$,TableWithReactTransition:E,TableWithSuspense:q,VirtualizedTable:D,VirtualizedTableWithEmptyStateStory:O,VirtualizedTableWithResizing:P,__namedExportsOrder:Qt,default:Et,makePromise:ne},Symbol.toStringTag,{value:"Module"}));export{T as M,J as T,di as a};
