import{j as a}from"./jsx-runtime-CDt2p4po.js";import{aW as l,aX as g,aY as c,q as j,r as v,O as P,aZ as e,B as C,a_ as w}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{r as R}from"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const L={title:"React Aria Components/Tabs",component:l},o=()=>{let[r,i]=R.useState("/FoR");return a.jsx(g,{navigate:i,children:a.jsxs(l,{selectedKey:r,children:[a.jsxs(c,{"aria-label":"History of Ancient Rome",style:{display:"flex",gap:8},children:[a.jsx(s,{id:"/FoR",href:"/FoR",children:"Founding of Rome"}),a.jsx(s,{id:"/MaR",href:"/MaR",children:"Monarchy and Republic"}),a.jsxs(j,{children:[a.jsx(s,{id:"/Emp",href:"/Emp",children:"Empire"}),a.jsxs(v,{offset:5,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:5,borderRadius:4},children:[a.jsx(P,{style:{transform:"translateX(-50%)"},children:a.jsx("svg",{width:"8",height:"8",style:{display:"block"},children:a.jsx("path",{d:"M0 0L4 4L8 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),"I am a tooltip"]})]})]}),a.jsx(e,{id:"/FoR",children:"Arma virumque cano, Troiae qui primus ab oris."}),a.jsx(e,{id:"/MaR",children:"Senatus Populusque Romanus."}),a.jsx(e,{id:"/Emp",children:"Alea jacta est."})]})})},t=()=>{const[r,i]=R.useState("vertical");return a.jsxs("div",{style:{display:"flex",flexDirection:"row",gap:8},children:[a.jsx(C,{onPress:()=>i(d=>d==="vertical"?"horizontal":"vertical"),children:"Change Orientation"}),a.jsx(l,{orientation:r,children:({orientation:d})=>a.jsx("div",{children:a.jsxs("div",{style:{display:"flex",flexDirection:d==="vertical"?"row":"column",gap:8},children:[a.jsxs(c,{"aria-label":"History of Ancient Rome",style:{display:"flex",flexDirection:d==="vertical"?"column":"row",gap:8},children:[a.jsx(s,{id:"FoR",children:"Founding of Rome"}),a.jsx(s,{id:"MaR",children:"Monarchy and Republic"}),a.jsx(s,{id:"Emp",children:"Empire"})]}),a.jsx(e,{id:"FoR",children:"Arma virumque cano, Troiae qui primus ab oris."}),a.jsx(e,{id:"MaR",children:"Senatus Populusque Romanus."}),a.jsx(e,{id:"Emp",children:"Alea jacta est."})]})})})]})},s=r=>a.jsx(w,{...r,style:({isSelected:i})=>({borderBottom:"2px solid "+(i?"slateblue":"transparent")})}),n=()=>a.jsxs(l,{children:[a.jsxs(c,{style:{display:"flex",gap:8},children:[a.jsx(s,{id:"foo",children:"Foo"}),a.jsx(s,{id:"bar",children:"Bar"})]}),a.jsx(e,{id:"foo",children:a.jsxs(l,{children:[a.jsxs(c,{style:{display:"flex",gap:8},children:[a.jsx(s,{id:"one",children:"One"}),a.jsx(s,{id:"two",children:"Two"})]}),a.jsx(e,{id:"one",children:"One"}),a.jsx(e,{id:"two",children:"Two"})]})}),a.jsx(e,{id:"bar",children:"Bar"})]});o.__docgenInfo={description:"",methods:[],displayName:"TabsExample"};t.__docgenInfo={description:"",methods:[],displayName:"TabsRenderProps"};n.__docgenInfo={description:"",methods:[],displayName:"NestedTabs"};var b,p,u;o.parameters={...o.parameters,docs:{...(b=o.parameters)==null?void 0:b.docs,source:{originalSource:`() => {
  let [url, setUrl] = useState('/FoR');
  return <RouterProvider navigate={setUrl}>
      <Tabs selectedKey={url}>
        <TabList aria-label="History of Ancient Rome" style={{
        display: 'flex',
        gap: 8
      }}>
          <CustomTab id="/FoR" href="/FoR">Founding of Rome</CustomTab>
          <CustomTab id="/MaR" href="/MaR">Monarchy and Republic</CustomTab>
          <TooltipTrigger>
            <CustomTab id="/Emp" href="/Emp">Empire</CustomTab>
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
        </TabList>
        <TabPanel id="/FoR">
          Arma virumque cano, Troiae qui primus ab oris.
        </TabPanel>
        <TabPanel id="/MaR">
          Senatus Populusque Romanus.
        </TabPanel>
        <TabPanel id="/Emp">
          Alea jacta est.
        </TabPanel>
      </Tabs>
    </RouterProvider>;
}`,...(u=(p=o.parameters)==null?void 0:p.docs)==null?void 0:u.source}}};var m,T,x;t.parameters={...t.parameters,docs:{...(m=t.parameters)==null?void 0:m.docs,source:{originalSource:`() => {
  const [tabOrientation, setTabOrientation] = useState<Orientation>('vertical');
  return <div style={{
    display: 'flex',
    flexDirection: 'row',
    gap: 8
  }}>
      <Button onPress={() => setTabOrientation(current => current === 'vertical' ? 'horizontal' : 'vertical')}>
        Change Orientation
      </Button>
      <Tabs orientation={tabOrientation}>
        {({
        orientation
      }) => <div>
            <div style={{
          display: 'flex',
          flexDirection: orientation === 'vertical' ? 'row' : 'column',
          gap: 8
        }}>
              <TabList aria-label="History of Ancient Rome" style={{
            display: 'flex',
            flexDirection: orientation === 'vertical' ? 'column' : 'row',
            gap: 8
          }}>
                <CustomTab id="FoR">Founding of Rome</CustomTab>
                <CustomTab id="MaR">Monarchy and Republic</CustomTab>
                <CustomTab id="Emp">Empire</CustomTab>
              </TabList>
              <TabPanel id="FoR">
                Arma virumque cano, Troiae qui primus ab oris.
              </TabPanel>
              <TabPanel id="MaR">
                Senatus Populusque Romanus.
              </TabPanel>
              <TabPanel id="Emp">
                Alea jacta est.
              </TabPanel>
            </div>
          </div>}
      </Tabs>
    </div>;
}`,...(x=(T=t.parameters)==null?void 0:T.docs)==null?void 0:x.source}}};var h,f,y;n.parameters={...n.parameters,docs:{...(h=n.parameters)==null?void 0:h.docs,source:{originalSource:`() => <Tabs>
    <TabList style={{
    display: 'flex',
    gap: 8
  }}>
      <CustomTab id="foo">Foo</CustomTab>
      <CustomTab id="bar">Bar</CustomTab>
    </TabList>
    <TabPanel id="foo">
      <Tabs>
        <TabList style={{
        display: 'flex',
        gap: 8
      }}>
          <CustomTab id="one">One</CustomTab>
          <CustomTab id="two">Two</CustomTab>
        </TabList>
        <TabPanel id="one">One</TabPanel>
        <TabPanel id="two">Two</TabPanel>
      </Tabs>
    </TabPanel>
    <TabPanel id="bar">Bar</TabPanel>
  </Tabs>`,...(y=(f=n.parameters)==null?void 0:f.docs)==null?void 0:y.source}}};const S=["TabsExample","TabsRenderProps","NestedTabs"];export{n as NestedTabs,o as TabsExample,t as TabsRenderProps,S as __namedExportsOrder,L as default};
