import{j as e}from"./jsx-runtime-CDt2p4po.js";import{ac as a,L as i,I as r,B as n,P as l,b as d,ad as ue,$ as be,V as me,h as xe}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{r as N}from"./index-GiUgBvb1.js";import{$ as ce,a as pe}from"./ListLayout-8Q9Kcx4Y.js";import{a as s,L as ye}from"./utils-N1pTmi3h.js";import{s as m}from"./index.module-B9nxguEg.js";/* empty css               */import"./index-C8NrMXaH.js";const Ve={title:"React Aria Components/ComboBox",component:a},u=()=>e.jsxs(a,{name:"combo-box-example","data-testid":"combo-box-example",allowsEmptyCollection:!0,children:[e.jsx(i,{style:{display:"block"},children:"Test"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(r,{}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:"▼"})})]}),e.jsx(l,{placement:"bottom end",children:e.jsxs(d,{renderEmptyState:T,"data-testid":"combo-box-list-box",className:m.menu,children:[e.jsx(s,{children:"Foo"}),e.jsx(s,{children:"Bar"}),e.jsx(s,{children:"Baz"}),e.jsx(s,{href:"http://google.com",children:"Google"}),e.jsx(V,{})]})})]});let f=[{id:"1",name:"Foo"},{id:"2",name:"Bar"},{id:"3",name:"Baz"}];const b=()=>e.jsx(a,{"data-testid":"combo-box-render-props-static",children:({isOpen:o})=>e.jsxs(e.Fragment,{children:[e.jsx(i,{style:{display:"block"},children:"Test"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(r,{}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:o?"▲":"▼"})})]}),e.jsx(l,{placement:"bottom end",children:e.jsxs(d,{className:m.menu,children:[e.jsx(s,{children:"Foo"}),e.jsx(s,{children:"Bar"}),e.jsx(s,{children:"Baz"})]})})]})}),B=()=>e.jsx(a,{defaultItems:f,children:({isOpen:o})=>e.jsxs(e.Fragment,{children:[e.jsx(i,{style:{display:"block"},children:"Test"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(r,{}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:o?"▲":"▼"})})]}),e.jsx(l,{placement:"bottom end",children:e.jsx(d,{className:m.menu,children:t=>e.jsx(s,{id:t.id,children:t.name})})})]})}),M={render:()=>e.jsx(a,{items:f,children:({isOpen:o})=>e.jsxs(e.Fragment,{children:[e.jsx(i,{style:{display:"block"},children:"Test"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(r,{}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:o?"▲":"▼"})})]}),e.jsx(l,{placement:"bottom end",children:e.jsx(d,{className:m.menu,children:t=>e.jsx(s,{id:t.id,children:t.name})})})]})}),parameters:{description:{data:"Note this won't filter the items in the listbox because it is fully controlled"}}},j=()=>e.jsx(a,{children:({isOpen:o})=>e.jsxs(e.Fragment,{children:[e.jsx(i,{style:{display:"block"},children:"Test"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(r,{}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:o?"▲":"▼"})})]}),e.jsx(l,{placement:"bottom end",children:e.jsx(d,{className:m.menu,items:f,children:t=>e.jsx(s,{id:t.id,children:t.name})})})]})}),L=()=>{let o=ce({async load({filterText:t}){return{items:await new Promise(x=>{setTimeout(()=>{x(t?f.filter(y=>{let c=y.name.toLowerCase();for(let h of t.toLowerCase()){if(!c.includes(h))return!1;c=c.replace(h,"")}return!0}):f)},300)})}}});return e.jsxs(a,{items:o.items,inputValue:o.filterText,onInputChange:o.setFilterText,children:[e.jsx(i,{style:{display:"block"},children:"Test"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(r,{}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:"▼"})})]}),e.jsx(l,{placement:"bottom end",children:e.jsx(d,{className:m.menu,children:t=>e.jsx(s,{children:t.name})})})]})},I=()=>e.jsxs(a,{children:[e.jsx(i,{style:{display:"block"},children:"IME Test"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(r,{}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:"▼"})})]}),e.jsx(l,{placement:"bottom end",children:e.jsxs(d,{"data-testid":"combo-box-list-box",className:m.menu,children:[e.jsx(s,{children:"にほんご"}),e.jsx(s,{children:"ニホンゴ"}),e.jsx(s,{children:"ﾆﾎﾝｺﾞ"}),e.jsx(s,{children:"日本語"}),e.jsx(s,{children:"123"}),e.jsx(s,{children:"１２３"})]})})]});let Be=[...Array(1e4)].map((o,t)=>({id:t,name:`Item ${t}`}));const je=o=>{const[t,p]=N.useState(""),{contains:x}=be({sensitivity:"base"}),y=N.useMemo(()=>Be.filter(c=>x(c.name,t)),[t,x]);return e.jsxs(a,{items:y,inputValue:t,onInputChange:p,children:[e.jsx(i,{style:{display:"block"},children:"Test"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(r,{}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:"▼"})})]}),e.jsx(l,{children:e.jsx(me,{layout:pe,layoutOptions:{rowHeight:25},children:e.jsxs(d,{className:m.menu,children:[e.jsx(xe,{items:y,children:c=>e.jsx(s,{children:c.name})}),e.jsx(V,{isLoading:o.isLoading})]})})})]})},v={render:o=>e.jsx(je,{...o}),args:{isLoading:!1}};let T=()=>e.jsx("div",{style:{height:30,width:"100%"},children:"No results"});const Le=o=>{let t=ce({async load({signal:p,cursor:x,filterText:y}){x&&(x=x.replace(/^http:\/\//i,"https://")),await new Promise(he=>setTimeout(he,o.delay));let h=await(await fetch(x||`https://swapi.py4e.com/api/people/?search=${y}`,{signal:p})).json();return{items:h.results,cursor:h.next}}});return e.jsxs(a,{inputValue:t.filterText,onInputChange:t.setFilterText,allowsEmptyCollection:!0,children:[e.jsx(i,{style:{display:"block"},children:"Async Virtualized Dynamic ComboBox"}),e.jsxs("div",{style:{display:"flex",position:"relative"},children:[e.jsx(r,{}),t.isLoading&&e.jsx(ye,{style:{left:"130px",top:"0px",height:20,width:20}}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:"▼"})})]}),e.jsx(l,{children:e.jsx(me,{layout:pe,layoutOptions:{rowHeight:25,loaderHeight:30},children:e.jsxs(d,{className:m.menu,renderEmptyState:T,children:[e.jsx(xe,{items:t.items,children:p=>e.jsx(s,{id:p.name,children:p.name})}),e.jsx(V,{isLoading:t.loadingState==="loadingMore",onLoadMore:t.loadMore})]})})})]})},P={render:o=>e.jsx(Le,{...o}),args:{delay:50}},V=o=>e.jsx(ue,{style:{height:30,width:"100%"},...o,children:e.jsx(ye,{style:{height:20,width:20,position:"unset"}})});function g(){let[o,t]=N.useState("");return e.jsxs(a,{allowsEmptyCollection:!0,inputValue:o,onInputChange:t,children:[e.jsx(i,{style:{display:"block"},children:"Favorite Animal"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(r,{}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:"▼"})})]}),e.jsx(l,{placement:"bottom end",children:e.jsxs(d,{"data-testid":"combo-box-list-box",className:m.menu,children:[o.length>0&&e.jsx(s,{onAction:()=>alert("hi"),children:`Create "${o}"`}),e.jsx(s,{children:"Aardvark"}),e.jsx(s,{children:"Cat"}),e.jsx(s,{children:"Dog"}),e.jsx(s,{children:"Kangaroo"}),e.jsx(s,{children:"Panda"}),e.jsx(s,{children:"Snake"})]})})]})}const C=()=>e.jsxs(a,{name:"combo-box-example","data-testid":"combo-box-example",allowsEmptyCollection:!0,children:[e.jsx(i,{style:{display:"block"},children:"Test"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(r,{}),e.jsx(n,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:"▼"})})]}),e.jsx(l,{placement:"bottom end",children:e.jsxs(d,{renderEmptyState:T,"data-testid":"combo-box-list-box",className:m.menu,children:[e.jsxs(s,{"aria-label":"Item Foo",textValue:"Foo",children:["Item ",e.jsx("b",{children:"Foo"})]}),e.jsxs(s,{"aria-label":"Item Bar",textValue:"Bar",children:["Item ",e.jsx("b",{children:"Bar"})]}),e.jsxs(s,{"aria-label":"Item Baz",textValue:"Baz",children:["Item ",e.jsx("b",{children:"Baz"})]})]})})]});u.__docgenInfo={description:"",methods:[],displayName:"ComboBoxExample"};b.__docgenInfo={description:"",methods:[],displayName:"ComboBoxRenderPropsStatic"};B.__docgenInfo={description:"",methods:[],displayName:"ComboBoxRenderPropsDefaultItems"};j.__docgenInfo={description:"",methods:[],displayName:"ComboBoxRenderPropsListBoxDynamic"};L.__docgenInfo={description:"",methods:[],displayName:"ComboBoxAsyncLoadingExample"};I.__docgenInfo={description:"",methods:[],displayName:"ComboBoxImeExample"};g.__docgenInfo={description:"",methods:[],displayName:"WithCreateOption"};C.__docgenInfo={description:"",methods:[],displayName:"ComboBoxListBoxItemWithAriaLabel"};var w,S,E;u.parameters={...u.parameters,docs:{...(w=u.parameters)==null?void 0:w.docs,source:{originalSource:`() => <ComboBox name="combo-box-example" data-testid="combo-box-example" allowsEmptyCollection>
    <Label style={{
    display: 'block'
  }}>Test</Label>
    <div style={{
    display: 'flex'
  }}>
      <Input />
      <Button>
        <span aria-hidden="true" style={{
        padding: '0 2px'
      }}>▼</span>
      </Button>
    </div>
    <Popover placement="bottom end">
      <ListBox renderEmptyState={renderEmptyState} data-testid="combo-box-list-box" className={styles.menu}>
        <MyListBoxItem>Foo</MyListBoxItem>
        <MyListBoxItem>Bar</MyListBoxItem>
        <MyListBoxItem>Baz</MyListBoxItem>
        <MyListBoxItem href="http://google.com">Google</MyListBoxItem>
        <MyListBoxLoaderIndicator />
      </ListBox>
    </Popover>
  </ComboBox>`,...(E=(S=u.parameters)==null?void 0:S.docs)==null?void 0:E.source}}};var k,z,A;b.parameters={...b.parameters,docs:{...(k=b.parameters)==null?void 0:k.docs,source:{originalSource:`() => <ComboBox data-testid="combo-box-render-props-static">
    {({
    isOpen
  }) => <>
        <Label style={{
      display: 'block'
    }}>Test</Label>
        <div style={{
      display: 'flex'
    }}>
          <Input />
          <Button>
            <span aria-hidden="true" style={{
          padding: '0 2px'
        }}>{isOpen ? '▲' : '▼'}</span>
          </Button>
        </div>
        <Popover placement="bottom end">
          <ListBox className={styles.menu}>
            <MyListBoxItem>Foo</MyListBoxItem>
            <MyListBoxItem>Bar</MyListBoxItem>
            <MyListBoxItem>Baz</MyListBoxItem>
          </ListBox>
        </Popover>
      </>}
  </ComboBox>`,...(A=(z=b.parameters)==null?void 0:z.docs)==null?void 0:A.source}}};var F,_,$;B.parameters={...B.parameters,docs:{...(F=B.parameters)==null?void 0:F.docs,source:{originalSource:`() => <ComboBox defaultItems={items}>
    {({
    isOpen
  }) => <>
        <Label style={{
      display: 'block'
    }}>Test</Label>
        <div style={{
      display: 'flex'
    }}>
          <Input />
          <Button>
            <span aria-hidden="true" style={{
          padding: '0 2px'
        }}>{isOpen ? '▲' : '▼'}</span>
          </Button>
        </div>
        <Popover placement="bottom end">
          <ListBox className={styles.menu}>
            {(item: ComboBoxItem) => <MyListBoxItem id={item.id}>{item.name}</MyListBoxItem>}
          </ListBox>
        </Popover>
      </>}
  </ComboBox>`,...($=(_=B.parameters)==null?void 0:_.docs)==null?void 0:$.source}}};var R,O,D;M.parameters={...M.parameters,docs:{...(R=M.parameters)==null?void 0:R.docs,source:{originalSource:`{
  render: () => <ComboBox items={items}>
      {({
      isOpen
    }) => <>
          <Label style={{
        display: 'block'
      }}>Test</Label>
          <div style={{
        display: 'flex'
      }}>
            <Input />
            <Button>
              <span aria-hidden="true" style={{
            padding: '0 2px'
          }}>{isOpen ? '▲' : '▼'}</span>
            </Button>
          </div>
          <Popover placement="bottom end">
            <ListBox className={styles.menu}>
              {(item: ComboBoxItem) => <MyListBoxItem id={item.id}>{item.name}</MyListBoxItem>}
            </ListBox>
          </Popover>
        </>}
    </ComboBox>,
  parameters: {
    description: {
      data: 'Note this won\\'t filter the items in the listbox because it is fully controlled'
    }
  }
}`,...(D=(O=M.parameters)==null?void 0:O.docs)==null?void 0:D.source}}};var W,H,G;j.parameters={...j.parameters,docs:{...(W=j.parameters)==null?void 0:W.docs,source:{originalSource:`() => <ComboBox>
    {({
    isOpen
  }) => <>
        <Label style={{
      display: 'block'
    }}>Test</Label>
        <div style={{
      display: 'flex'
    }}>
          <Input />
          <Button>
            <span aria-hidden="true" style={{
          padding: '0 2px'
        }}>{isOpen ? '▲' : '▼'}</span>
          </Button>
        </div>
        <Popover placement="bottom end">
          <ListBox className={styles.menu} items={items}>
            {item => <MyListBoxItem id={item.id}>{item.name}</MyListBoxItem>}
          </ListBox>
        </Popover>
      </>}
  </ComboBox>`,...(G=(H=j.parameters)==null?void 0:H.docs)==null?void 0:G.source}}};var K,q,J;L.parameters={...L.parameters,docs:{...(K=L.parameters)==null?void 0:K.docs,source:{originalSource:`() => {
  let list = useAsyncList<ComboBoxItem>({
    async load({
      filterText
    }) {
      let json = (await new Promise(resolve => {
        setTimeout(() => {
          resolve(filterText ? items.filter(item => {
            let name = item.name.toLowerCase();
            for (let filterChar of filterText.toLowerCase()) {
              if (!name.includes(filterChar)) {
                return false;
              }
              name = name.replace(filterChar, '');
            }
            return true;
          }) : items);
        }, 300);
      })) as ComboBoxItem[];
      return {
        items: json
      };
    }
  });
  return <ComboBox items={list.items} inputValue={list.filterText} onInputChange={list.setFilterText}>
      <Label style={{
      display: 'block'
    }}>Test</Label>
      <div style={{
      display: 'flex'
    }}>
        <Input />
        <Button>
          <span aria-hidden="true" style={{
          padding: '0 2px'
        }}>▼</span>
        </Button>
      </div>
      <Popover placement="bottom end">
        <ListBox<ComboBoxItem> className={styles.menu}>
          {item => <MyListBoxItem>{item.name}</MyListBoxItem>}
        </ListBox>
      </Popover>
    </ComboBox>;
}`,...(J=(q=L.parameters)==null?void 0:q.docs)==null?void 0:J.source}}};var Q,U,X;I.parameters={...I.parameters,docs:{...(Q=I.parameters)==null?void 0:Q.docs,source:{originalSource:`() => <ComboBox>
    <Label style={{
    display: 'block'
  }}>IME Test</Label>
    <div style={{
    display: 'flex'
  }}>
      <Input />
      <Button>
        <span aria-hidden="true" style={{
        padding: '0 2px'
      }}>▼</span>
      </Button>
    </div>
    <Popover placement="bottom end">
      <ListBox data-testid="combo-box-list-box" className={styles.menu}>
        <MyListBoxItem>にほんご</MyListBoxItem>
        <MyListBoxItem>ニホンゴ</MyListBoxItem>
        <MyListBoxItem>ﾆﾎﾝｺﾞ</MyListBoxItem>
        <MyListBoxItem>日本語</MyListBoxItem>
        <MyListBoxItem>123</MyListBoxItem>
        <MyListBoxItem>１２３</MyListBoxItem>
      </ListBox>
    </Popover>
  </ComboBox>`,...(X=(U=I.parameters)==null?void 0:U.docs)==null?void 0:X.source}}};var Y,Z,ee;v.parameters={...v.parameters,docs:{...(Y=v.parameters)==null?void 0:Y.docs,source:{originalSource:`{
  render: args => <VirtualizedComboBoxRender {...args} />,
  args: {
    isLoading: false
  }
}`,...(ee=(Z=v.parameters)==null?void 0:Z.docs)==null?void 0:ee.source}}};var te,se,oe;P.parameters={...P.parameters,docs:{...(te=P.parameters)==null?void 0:te.docs,source:{originalSource:`{
  render: args => <AsyncVirtualizedDynamicComboboxRender {...args} />,
  args: {
    delay: 50
  }
}`,...(oe=(se=P.parameters)==null?void 0:se.docs)==null?void 0:oe.source}}};var ae,ie,re;g.parameters={...g.parameters,docs:{...(ae=g.parameters)==null?void 0:ae.docs,source:{originalSource:`function WithCreateOption() {
  let [inputValue, setInputValue] = useState('');
  return <ComboBox allowsEmptyCollection inputValue={inputValue} onInputChange={setInputValue}>
      <Label style={{
      display: 'block'
    }}>Favorite Animal</Label>
      <div style={{
      display: 'flex'
    }}>
        <Input />
        <Button>
          <span aria-hidden="true" style={{
          padding: '0 2px'
        }}>▼</span>
        </Button>
      </div>
      <Popover placement="bottom end">
        <ListBox data-testid="combo-box-list-box" className={styles.menu}>
          {inputValue.length > 0 && <MyListBoxItem onAction={() => alert('hi')}>
              {\`Create "\${inputValue}"\`}
            </MyListBoxItem>}
          <MyListBoxItem>Aardvark</MyListBoxItem>
          <MyListBoxItem>Cat</MyListBoxItem>
          <MyListBoxItem>Dog</MyListBoxItem>
          <MyListBoxItem>Kangaroo</MyListBoxItem>
          <MyListBoxItem>Panda</MyListBoxItem>
          <MyListBoxItem>Snake</MyListBoxItem>
        </ListBox>
      </Popover>
    </ComboBox>;
}`,...(re=(ie=g.parameters)==null?void 0:ie.docs)==null?void 0:re.source}}};var ne,le,de;C.parameters={...C.parameters,docs:{...(ne=C.parameters)==null?void 0:ne.docs,source:{originalSource:`() => <ComboBox name="combo-box-example" data-testid="combo-box-example" allowsEmptyCollection>
    <Label style={{
    display: 'block'
  }}>Test</Label>
    <div style={{
    display: 'flex'
  }}>
      <Input />
      <Button>
        <span aria-hidden="true" style={{
        padding: '0 2px'
      }}>▼</span>
      </Button>
    </div>
    <Popover placement="bottom end">
      <ListBox renderEmptyState={renderEmptyState} data-testid="combo-box-list-box" className={styles.menu}>
        <MyListBoxItem aria-label="Item Foo" textValue="Foo">Item <b>Foo</b></MyListBoxItem>
        <MyListBoxItem aria-label="Item Bar" textValue="Bar">Item <b>Bar</b></MyListBoxItem>
        <MyListBoxItem aria-label="Item Baz" textValue="Baz">Item <b>Baz</b></MyListBoxItem>
      </ListBox>
    </Popover>
  </ComboBox>`,...(de=(le=C.parameters)==null?void 0:le.docs)==null?void 0:de.source}}};const we=["ComboBoxExample","ComboBoxRenderPropsStatic","ComboBoxRenderPropsDefaultItems","ComboBoxRenderPropsItems","ComboBoxRenderPropsListBoxDynamic","ComboBoxAsyncLoadingExample","ComboBoxImeExample","VirtualizedComboBox","AsyncVirtualizedDynamicCombobox","WithCreateOption","ComboBoxListBoxItemWithAriaLabel"];export{P as AsyncVirtualizedDynamicCombobox,L as ComboBoxAsyncLoadingExample,u as ComboBoxExample,I as ComboBoxImeExample,C as ComboBoxListBoxItemWithAriaLabel,B as ComboBoxRenderPropsDefaultItems,M as ComboBoxRenderPropsItems,j as ComboBoxRenderPropsListBoxDynamic,b as ComboBoxRenderPropsStatic,v as VirtualizedComboBox,g as WithCreateOption,we as __namedExportsOrder,Ve as default};
