import{j as e}from"./jsx-runtime-CDt2p4po.js";import{a as k}from"./index-B-lxVbXh.js";import{G as c,B as n,as as ce,i as T,j as M,V as b,h as j,at as v,o as B,p as w,au as h,X as me,av as ue,aw as he,ax as pe,a4 as ge,E as xe,ay as ye,D as Le,P as je}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{r as A}from"./index-GiUgBvb1.js";import{$ as Ge}from"./GridLayout-Bc3SIaYk.js";import{a as z,b as fe,$ as oe}from"./ListLayout-8Q9Kcx4Y.js";import{u as Ie}from"./useDragAndDrop--5mYXGU7.js";import{c as Se,L as de}from"./utils-N1pTmi3h.js";import{s as m}from"./index.module-B9nxguEg.js";/* empty css               */import"./v4-CtRu48qb.js";import"./index-C8NrMXaH.js";import"./useDrag-D4nPEkp-.js";const We={title:"React Aria Components/GridList",component:c,excludeStories:["MyGridListItem"]},p=t=>e.jsxs(c,{...t,className:m.menu,"aria-label":"test gridlist",style:{width:300,height:300,display:"grid",gridTemplate:t.layout==="grid"?"repeat(3, 1fr) / repeat(3, 1fr)":"auto / 1fr",gridAutoFlow:"row"},children:[e.jsxs(r,{textValue:"1,1",children:["1,1 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{textValue:"1,2",children:["1,2 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{textValue:"1,3",children:["1,3 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{textValue:"2,1",children:["2,1 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{textValue:"2,2",children:["2,2 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{textValue:"2,3",children:["2,3 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{textValue:"3,1",children:["3,1 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{textValue:"3,2",children:["3,2 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{textValue:"3,3",children:["3,3 ",e.jsx(n,{children:"Actions"})]})]}),r=t=>e.jsx(ce,{...t,style:{display:"flex",alignItems:"center",gap:8},className:({isFocused:i,isSelected:s,isHovered:o})=>Se(m,"item",{focused:i,selected:s,hovered:o}),children:({selectionMode:i,allowsDragging:s})=>e.jsxs(e.Fragment,{children:[s&&e.jsx(n,{slot:"drag",children:"≡"}),i!=="none"?e.jsx(Te,{slot:"selection"}):null,t.children]})});p.story={args:{layout:"stack",escapeKeyBehavior:"clearSelection",shouldSelectOnPressUp:!1,disallowTypeAhead:!1},argTypes:{layout:{control:"radio",options:["stack","grid"]},keyboardNavigationBehavior:{control:"radio",options:["arrow","tab"]},selectionMode:{control:"radio",options:["none","single","multiple"]},selectionBehavior:{control:"radio",options:["toggle","replace"]},escapeKeyBehavior:{control:"radio",options:["clearSelection","none"]}}};const Te=({children:t,...i})=>e.jsx(me,{...i,children:({isIndeterminate:s})=>e.jsxs(e.Fragment,{children:[e.jsx("div",{className:"checkbox",children:e.jsx("svg",{viewBox:"0 0 18 18","aria-hidden":"true",children:s?e.jsx("rect",{x:1,y:7.5,width:15,height:3}):e.jsx("polyline",{points:"1 9 7 14 15 4"})})}),t]})}),g=t=>e.jsxs(c,{...t,className:m.menu,"aria-label":"test gridlist",style:{width:400,height:400},children:[e.jsxs(T,{children:[e.jsx(M,{children:"Section 1"}),e.jsxs(r,{children:["1,1 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{children:["1,2 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{children:["1,3 ",e.jsx(n,{children:"Actions"})]})]}),e.jsxs(T,{children:[e.jsx(M,{children:"Section 2"}),e.jsxs(r,{children:["2,1 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{children:["2,2 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{children:["2,3 ",e.jsx(n,{children:"Actions"})]})]}),e.jsxs(T,{children:[e.jsx(M,{children:"Section 3"}),e.jsxs(r,{children:["3,1 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{children:["3,2 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{children:["3,3 ",e.jsx(n,{children:"Actions"})]})]})]});g.story={args:{layout:"stack",escapeKeyBehavior:"clearSelection",shouldSelectOnPressUp:!1},argTypes:{layout:{control:"radio",options:["stack","grid"]},keyboardNavigationBehavior:{control:"radio",options:["arrow","tab"]},selectionMode:{control:"radio",options:["none","single","multiple"]},selectionBehavior:{control:"radio",options:["toggle","replace"]},escapeKeyBehavior:{control:"radio",options:["clearSelection","none"]}}};function y(){let t=[];for(let i=0;i<10;i++){let s=[];for(let o=0;o<3;o++)s.push({id:`item_${i}_${o}`,name:`Section ${i}, Item ${o}`});t.push({id:`section_${i}`,name:`Section ${i}`,children:s})}return e.jsx(b,{layout:z,layoutOptions:{rowHeight:25},children:e.jsx(c,{className:m.menu,style:{height:400},"aria-label":"virtualized with grid section",items:t,children:e.jsx(j,{items:t,children:i=>e.jsxs(T,{children:[e.jsx(M,{children:i.name}),e.jsx(j,{items:i.children,children:s=>e.jsx(r,{children:s.name})})]})})})})}const Me=t=>{let i=[];for(let a=0;a<1e4;a++)i.push({id:a,name:`Item ${a}`});let s=fe({initialItems:i}),{dragAndDropHooks:o}=Ie({getItems:a=>[...a].map(u=>{var d;return{"text/plain":((d=s.getItem(u))==null?void 0:d.name)??""}}),onReorder(a){a.target.dropPosition==="before"?s.moveBefore(a.target.key,a.keys):a.target.dropPosition==="after"&&s.moveAfter(a.target.key,a.keys)},renderDropIndicator(a){return e.jsx(ue,{target:a,style:({isDropTarget:u})=>({width:"100%",height:"100%",background:u?"blue":"transparent"})})}});return e.jsx(b,{layout:z,layoutOptions:{rowHeight:25},children:e.jsxs(c,{className:m.menu,selectionMode:"multiple",dragAndDropHooks:o,style:{height:400},"aria-label":"virtualized gridlist",items:s.items,children:[e.jsx(j,{items:s.items,children:a=>e.jsx(r,{children:a.name})}),e.jsx(V,{isLoading:t.isLoading})]})})},G={render:t=>e.jsx(Me,{...t}),args:{isLoading:!1}};let x=t=>{const{minItemSizeWidth:i=40,maxItemSizeWidth:s=65,maxColumns:o=1/0,minHorizontalSpace:a=0,maxHorizontalSpace:u=1/0}=t;let d=[];for(let l=0;l<1e4;l++)d.push({id:l,name:`Item ${l}`});return e.jsx(b,{layout:Ge,layoutOptions:{minItemSize:new v(i,40),maxItemSize:new v(s,40),minSpace:new v(a,18),maxColumns:o,maxHorizontalSpace:u},children:e.jsx(c,{className:m.menu,layout:"grid",style:{height:400,width:400},"aria-label":"virtualized listbox",items:d,children:l=>e.jsx(r,{children:l.name})})})};x.story={args:{minItemSizeWidth:40,maxItemSizeWidth:65,maxColumns:void 0,minHorizontalSpace:0,maxHorizontalSpace:void 0},argTypes:{minItemSizeWidth:{control:"number",description:"The minimum width of each item in the grid list",defaultValue:40},maxItemSizeWidth:{control:"number",description:"Maximum width of each item in the grid list.",defaultValue:65},maxColumns:{control:"number",description:"Maximum number of columns in the grid list.",defaultValue:void 0},minHorizontalSpace:{control:"number",description:"Minimum horizontal space between grid items.",defaultValue:0},maxHorizontalSpace:{control:"number",description:"Maximum horizontal space between grid items.",defaultValue:void 0}}};let le=({isLoading:t})=>e.jsx("div",{style:{height:30,width:"100%"},children:t?e.jsx(de,{style:{height:20,width:20,transform:"translate(-50%, -50%)"}}):"No results"});const V=t=>e.jsx(ye,{style:{height:30,width:"100%",display:"flex",alignItems:"center",justifyContent:"center"},...t,children:e.jsx(de,{style:{height:20,width:20,position:"unset"}})});function be(t){let i=oe({async load({signal:s,cursor:o,filterText:a}){o&&(o=o.replace(/^http:\/\//i,"https://")),await new Promise(l=>setTimeout(l,t.delay));let d=await(await fetch(o||`https://swapi.py4e.com/api/people/?search=${a}`,{signal:s})).json();return{items:d.results,cursor:d.next}}});return e.jsxs(c,{className:m.menu,style:{height:200},"aria-label":"async gridlist",renderEmptyState:()=>le({isLoading:i.isLoading}),children:[e.jsx(j,{items:i.items,children:s=>e.jsx(r,{id:s.name,children:s.name})}),e.jsx(V,{isLoading:i.loadingState==="loadingMore",onLoadMore:i.loadMore})]})}let f={render:t=>e.jsx(be,{...t}),args:{delay:50}};function ve(t){let i=oe({async load({signal:s,cursor:o,filterText:a}){o&&(o=o.replace(/^http:\/\//i,"https://")),await new Promise(l=>setTimeout(l,t.delay));let d=await(await fetch(o||`https://swapi.py4e.com/api/people/?search=${a}`,{signal:s})).json();return{items:d.results,cursor:d.next}}});return e.jsx(b,{layout:z,layoutOptions:{rowHeight:25,loaderHeight:30},children:e.jsxs(c,{className:m.menu,style:{height:200},"aria-label":"async virtualized gridlist",renderEmptyState:()=>le({isLoading:i.isLoading}),children:[e.jsx(j,{items:i.items,children:s=>e.jsx(r,{id:s.name,children:s.name})}),e.jsx(V,{isLoading:i.loadingState==="loadingMore",onLoadMore:i.loadMore})]})})}let I={render:t=>e.jsx(ve,{...t}),args:{delay:50}},L=()=>e.jsxs(c,{className:m.menu,"aria-label":"Grid list with tag group",keyboardNavigationBehavior:"tab",style:{width:300,height:300},children:[e.jsxs(r,{textValue:"Tags",children:["1,1",e.jsx(B,{"aria-label":"Tag group 1",onRemove:k("onRemove"),children:e.jsxs(w,{style:{display:"flex",gap:10},children:[e.jsxs(h,{children:["Tag 1",e.jsx(n,{slot:"remove",children:"X"})]},"1"),e.jsxs(h,{children:["Tag 2",e.jsx(n,{slot:"remove",children:"X"})]},"2"),e.jsxs(h,{children:["Tag 3",e.jsx(n,{slot:"remove",children:"X"})]},"3")]})}),e.jsx(B,{"aria-label":"Tag group 2",onRemove:k("onRemove"),children:e.jsxs(w,{style:{display:"flex",gap:10},children:[e.jsxs(h,{children:["Tag 1",e.jsx(n,{slot:"remove",children:"X"})]},"1"),e.jsxs(h,{children:["Tag 2",e.jsx(n,{slot:"remove",children:"X"})]},"2"),e.jsxs(h,{children:["Tag 3",e.jsx(n,{slot:"remove",children:"X"})]},"3")]})})]}),e.jsxs(r,{children:["1,2 ",e.jsx(n,{children:"Actions"})]}),e.jsxs(r,{children:["1,3",e.jsx(B,{"aria-label":"Tag group",children:e.jsxs(w,{style:{display:"flex",gap:10},children:[e.jsx(h,{children:"Tag 1"},"1"),e.jsx(h,{children:"Tag 2"},"2"),e.jsx(h,{children:"Tag 3"},"3")]})})]})]});const Be=()=>{const[t,i]=A.useState(!1),[s,o]=A.useState(new Set([])),a=u=>{o(u),i(!1)};return e.jsxs(Le,{isOpen:t,onOpenChange:i,children:[e.jsx(n,{children:"Open GridList Options"}),e.jsx(je,{children:e.jsx("div",{children:e.jsxs(c,{className:m.menu,selectedKeys:s,"aria-label":"Favorite pokemon",selectionMode:"single",onSelectionChange:a,shouldSelectOnPressUp:!0,autoFocus:!0,children:[e.jsxs(r,{textValue:"Charizard",children:["Option 1 ",e.jsx(n,{children:"A"})]}),e.jsxs(r,{textValue:"Blastoise",children:["Option 2 ",e.jsx(n,{children:"B"})]}),e.jsxs(r,{textValue:"Venusaur",children:["Option 3 ",e.jsx(n,{children:"C"})]}),e.jsxs(r,{textValue:"Pikachu",children:["Option 4 ",e.jsx(n,{children:"D"})]})]})})})]})};function we(t){const[i,s]=A.useState(!0);return e.jsxs(e.Fragment,{children:[e.jsx(n,{onPress:()=>s(!0),children:"Open Modal"}),e.jsx(he,{...t,isOpen:i,onOpenChange:s,isDismissable:!0,style:{position:"fixed",top:0,left:0,width:"100%",height:"100%",background:"rgba(0,0,0,0.5)"},children:e.jsx(pe,{children:e.jsx(ge,{children:e.jsxs("div",{style:{display:"flex",flexDirection:"column",padding:8,background:"#ccc",position:"absolute",top:"50%",left:"50%",transform:"translate(-50%,-50%)",width:"max-content",height:"max-content"},children:[e.jsx(xe,{slot:"title",children:"Open the GridList Picker"}),e.jsx(Be,{})]})})})})]})}let S={render:t=>e.jsx(we,{...t}),parameters:{docs:{description:{component:"Selecting an option from the grid list over the backdrop should not result in the modal closing."}}}};p.__docgenInfo={description:"",methods:[],displayName:"GridListExample"};r.__docgenInfo={description:"",methods:[],displayName:"MyGridListItem",props:{className:{required:!1,tsType:{name:"union",raw:"string | ((values: T & {defaultClassName: string | undefined}) => string)",elements:[{name:"string"},{name:"unknown"}]},description:"The CSS [className](https://developer.mozilla.org/en-US/docs/Web/API/Element/className) for the element. A function may be provided to compute the class based on component state."},style:{required:!1,tsType:{name:"union",raw:"CSSProperties | ((values: T & {defaultStyle: CSSProperties}) => CSSProperties | undefined)",elements:[{name:"CSSProperties"},{name:"unknown"}]},description:"The inline [style](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style) for the element. A function may be provided to compute the style based on component state."},children:{required:!1,tsType:{name:"union",raw:"ReactNode | ((values: T & {defaultChildren: ReactNode | undefined}) => ReactNode)",elements:[{name:"ReactNode"},{name:"unknown"}]},description:"The children of the component. A function may be provided to alter the children based on component state."},id:{required:!1,tsType:{name:"Key"},description:"The unique id of the item."},value:{required:!1,tsType:{name:"T"},description:"The object value that this item represents. When using dynamic collections, this is set automatically."},textValue:{required:!1,tsType:{name:"string"},description:"A string representation of the item's contents, used for features like typeahead."},isDisabled:{required:!1,tsType:{name:"boolean"},description:"Whether the item is disabled."},onAction:{required:!1,tsType:{name:"signature",type:"function",raw:"() => void",signature:{arguments:[],return:{name:"void"}}},description:"Handler that is called when a user performs an action on the item. The exact user event depends on\nthe collection's `selectionBehavior` prop and the interaction modality."}},composes:["LinkDOMProps","HoverEvents","PressEvents","Omit"]};g.__docgenInfo={description:"",methods:[],displayName:"GridListSectionExample"};y.__docgenInfo={description:"",methods:[],displayName:"VirtualizedGridListSection"};x.__docgenInfo={description:"",methods:[],displayName:"VirtualizedGridListGrid"};L.__docgenInfo={description:"",methods:[],displayName:"TagGroupInsideGridList"};var $,N,H;p.parameters={...p.parameters,docs:{...($=p.parameters)==null?void 0:$.docs,source:{originalSource:`args => <GridList {...args} className={styles.menu} aria-label="test gridlist" style={{
  width: 300,
  height: 300,
  display: 'grid',
  gridTemplate: args.layout === 'grid' ? 'repeat(3, 1fr) / repeat(3, 1fr)' : 'auto / 1fr',
  gridAutoFlow: 'row'
}}>
    <MyGridListItem textValue="1,1">1,1 <Button>Actions</Button></MyGridListItem>
    <MyGridListItem textValue="1,2">1,2 <Button>Actions</Button></MyGridListItem>
    <MyGridListItem textValue="1,3">1,3 <Button>Actions</Button></MyGridListItem>
    <MyGridListItem textValue="2,1">2,1 <Button>Actions</Button></MyGridListItem>
    <MyGridListItem textValue="2,2">2,2 <Button>Actions</Button></MyGridListItem>
    <MyGridListItem textValue="2,3">2,3 <Button>Actions</Button></MyGridListItem>
    <MyGridListItem textValue="3,1">3,1 <Button>Actions</Button></MyGridListItem>
    <MyGridListItem textValue="3,2">3,2 <Button>Actions</Button></MyGridListItem>
    <MyGridListItem textValue="3,3">3,3 <Button>Actions</Button></MyGridListItem>
  </GridList>`,...(H=(N=p.parameters)==null?void 0:N.docs)==null?void 0:H.source}}};var O,C,P;g.parameters={...g.parameters,docs:{...(O=g.parameters)==null?void 0:O.docs,source:{originalSource:`args => <GridList {...args} className={styles.menu} aria-label="test gridlist" style={{
  width: 400,
  height: 400
}}>
    <GridListSection>
      <GridListHeader>Section 1</GridListHeader>
      <MyGridListItem>1,1 <Button>Actions</Button></MyGridListItem>
      <MyGridListItem>1,2 <Button>Actions</Button></MyGridListItem>
      <MyGridListItem>1,3 <Button>Actions</Button></MyGridListItem>
    </GridListSection>
    <GridListSection>
      <GridListHeader>Section 2</GridListHeader>
      <MyGridListItem>2,1 <Button>Actions</Button></MyGridListItem>
      <MyGridListItem>2,2 <Button>Actions</Button></MyGridListItem>
      <MyGridListItem>2,3 <Button>Actions</Button></MyGridListItem>
    </GridListSection>
    <GridListSection>
      <GridListHeader>Section 3</GridListHeader>
      <MyGridListItem>3,1 <Button>Actions</Button></MyGridListItem>
      <MyGridListItem>3,2 <Button>Actions</Button></MyGridListItem>
      <MyGridListItem>3,3 <Button>Actions</Button></MyGridListItem>
    </GridListSection>
  </GridList>`,...(P=(C=g.parameters)==null?void 0:C.docs)==null?void 0:P.source}}};var R,_,E;y.parameters={...y.parameters,docs:{...(R=y.parameters)==null?void 0:R.docs,source:{originalSource:`function VirtualizedGridListSection() {
  let sections: {
    id: string;
    name: string;
    children: {
      id: string;
      name: string;
    }[];
  }[] = [];
  for (let s = 0; s < 10; s++) {
    let items: {
      id: string;
      name: string;
    }[] = [];
    for (let i = 0; i < 3; i++) {
      items.push({
        id: \`item_\${s}_\${i}\`,
        name: \`Section \${s}, Item \${i}\`
      });
    }
    sections.push({
      id: \`section_\${s}\`,
      name: \`Section \${s}\`,
      children: items
    });
  }
  return <Virtualizer layout={ListLayout} layoutOptions={{
    rowHeight: 25
  }}>
      <GridList className={styles.menu}
    // selectionMode="multiple"
    style={{
      height: 400
    }} aria-label="virtualized with grid section" items={sections}>
        <Collection items={sections}>
          {section => <GridListSection>
              <GridListHeader>{section.name}</GridListHeader>
              <Collection items={section.children}>
                {item => <MyGridListItem>{item.name}</MyGridListItem>}
              </Collection>
            </GridListSection>}
        </Collection>
      </GridList>
    </Virtualizer>;
}`,...(E=(_=y.parameters)==null?void 0:_.docs)==null?void 0:E.source}}};var D,W,X;G.parameters={...G.parameters,docs:{...(D=G.parameters)==null?void 0:D.docs,source:{originalSource:`{
  render: args => <VirtualizedGridListRender {...args} />,
  args: {
    isLoading: false
  }
}`,...(X=(W=G.parameters)==null?void 0:W.docs)==null?void 0:X.source}}};var q,F,K;x.parameters={...x.parameters,docs:{...(q=x.parameters)==null?void 0:q.docs,source:{originalSource:`args => {
  const {
    minItemSizeWidth = 40,
    maxItemSizeWidth = 65,
    maxColumns = Infinity,
    minHorizontalSpace = 0,
    maxHorizontalSpace = Infinity
  } = args;
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
  return <Virtualizer layout={GridLayout} layoutOptions={{
    minItemSize: new Size(minItemSizeWidth, 40),
    maxItemSize: new Size(maxItemSizeWidth, 40),
    minSpace: new Size(minHorizontalSpace, 18),
    maxColumns,
    maxHorizontalSpace
  }}>
      <GridList className={styles.menu} layout="grid" style={{
      height: 400,
      width: 400
    }} aria-label="virtualized listbox" items={items}>
        {item => <MyGridListItem>{item.name}</MyGridListItem>}
      </GridList>
    </Virtualizer>;
}`,...(K=(F=x.parameters)==null?void 0:F.docs)==null?void 0:K.source}}};var U,J,Q;f.parameters={...f.parameters,docs:{...(U=f.parameters)==null?void 0:U.docs,source:{originalSource:`{
  render: args => <AsyncGridListRender {...args} />,
  args: {
    delay: 50
  }
}`,...(Q=(J=f.parameters)==null?void 0:J.docs)==null?void 0:Q.source}}};var Y,Z,ee;I.parameters={...I.parameters,docs:{...(Y=I.parameters)==null?void 0:Y.docs,source:{originalSource:`{
  render: args => <AsyncGridListVirtualizedRender {...args} />,
  args: {
    delay: 50
  }
}`,...(ee=(Z=I.parameters)==null?void 0:Z.docs)==null?void 0:ee.source}}};var te,ie,se;L.parameters={...L.parameters,docs:{...(te=L.parameters)==null?void 0:te.docs,source:{originalSource:`() => {
  return <GridList className={styles.menu} aria-label="Grid list with tag group" keyboardNavigationBehavior="tab" style={{
    width: 300,
    height: 300
  }}>
      <MyGridListItem textValue="Tags">
        1,1
        <TagGroup aria-label="Tag group 1" onRemove={action('onRemove')}>
          <TagList style={{
          display: 'flex',
          gap: 10
        }}>
            <Tag key="1">Tag 1<Button slot="remove">X</Button></Tag>
            <Tag key="2">Tag 2<Button slot="remove">X</Button></Tag>
            <Tag key="3">Tag 3<Button slot="remove">X</Button></Tag>
          </TagList>
        </TagGroup>
        <TagGroup aria-label="Tag group 2" onRemove={action('onRemove')}>
          <TagList style={{
          display: 'flex',
          gap: 10
        }}>
            <Tag key="1">Tag 1<Button slot="remove">X</Button></Tag>
            <Tag key="2">Tag 2<Button slot="remove">X</Button></Tag>
            <Tag key="3">Tag 3<Button slot="remove">X</Button></Tag>
          </TagList>
        </TagGroup>
      </MyGridListItem>
      <MyGridListItem>
        1,2 <Button>Actions</Button>
      </MyGridListItem>
      <MyGridListItem>
        1,3
        <TagGroup aria-label="Tag group">
          <TagList style={{
          display: 'flex',
          gap: 10
        }}>
            <Tag key="1">Tag 1</Tag>
            <Tag key="2">Tag 2</Tag>
            <Tag key="3">Tag 3</Tag>
          </TagList>
        </TagGroup>
      </MyGridListItem>
    </GridList>;
}`,...(se=(ie=L.parameters)==null?void 0:ie.docs)==null?void 0:se.source}}};var ne,re,ae;S.parameters={...S.parameters,docs:{...(ne=S.parameters)==null?void 0:ne.docs,source:{originalSource:`{
  render: args => <GridListInModalPickerRender {...args} />,
  parameters: {
    docs: {
      description: {
        component: 'Selecting an option from the grid list over the backdrop should not result in the modal closing.'
      }
    }
  }
}`,...(ae=(re=S.parameters)==null?void 0:re.docs)==null?void 0:ae.source}}};const Xe=["GridListExample","MyGridListItem","GridListSectionExample","VirtualizedGridListSection","VirtualizedGridList","VirtualizedGridListGrid","AsyncGridList","AsyncGridListVirtualized","TagGroupInsideGridList","GridListInModalPicker"];export{f as AsyncGridList,I as AsyncGridListVirtualized,p as GridListExample,S as GridListInModalPicker,g as GridListSectionExample,r as MyGridListItem,L as TagGroupInsideGridList,G as VirtualizedGridList,x as VirtualizedGridListGrid,y as VirtualizedGridListSection,Xe as __namedExportsOrder,We as default};
