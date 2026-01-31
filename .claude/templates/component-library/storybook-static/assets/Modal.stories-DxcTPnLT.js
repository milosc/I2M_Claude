import{j as e}from"./jsx-runtime-CDt2p4po.js";import{ax as i,D as l,B as s,aw as u,a4 as a,E as j,T as y,L as n,I as d,P as f,ac as T,b as C}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";/* empty css               */import{a as t}from"./utils-N1pTmi3h.js";import{s as I}from"./index.module-B9nxguEg.js";import"./index-C8NrMXaH.js";const L={title:"React Aria Components/Modal",component:i},o=()=>e.jsxs(l,{children:[e.jsx(s,{children:"Open modal"}),e.jsx(u,{style:{position:"fixed",zIndex:100,top:0,left:0,bottom:0,right:0,background:"rgba(0, 0, 0, 0.5)",display:"flex",alignItems:"center",justifyContent:"center"},children:e.jsx(i,{style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:30},children:e.jsx(a,{children:({close:b})=>e.jsxs("form",{style:{display:"flex",flexDirection:"column"},children:[e.jsx(j,{slot:"title",style:{marginTop:0},children:"Sign up"}),e.jsxs("label",{children:["First Name: ",e.jsx("input",{placeholder:"John"})]}),e.jsxs("label",{children:["Last Name: ",e.jsx("input",{placeholder:"Smith"})]}),e.jsx(s,{onPress:b,style:{marginTop:10},children:"Submit"})]})})})})]});function k(){return e.jsxs(l,{children:[e.jsx(s,{children:"Open modal"}),e.jsx(u,{isDismissable:!0,style:{position:"fixed",zIndex:100,top:0,left:0,bottom:0,right:0,background:"rgba(0, 0, 0, 0.5)",display:"flex",alignItems:"center",justifyContent:"center"},children:e.jsx(i,{style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:30},children:e.jsx(a,{children:()=>e.jsxs(e.Fragment,{children:[e.jsxs(y,{children:[e.jsx(n,{children:"First name"}),e.jsx(d,{})]}),e.jsxs(l,{children:[e.jsx(s,{children:"Combobox Trigger"}),e.jsx(f,{placement:"bottom start",children:e.jsx(a,{children:()=>e.jsxs(T,{menuTrigger:"focus",autoFocus:!0,name:"combo-box-example","data-testid":"combo-box-example",allowsEmptyCollection:!0,children:[e.jsx(n,{style:{display:"block"},children:"Test"}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx(d,{}),e.jsx(s,{children:e.jsx("span",{"aria-hidden":"true",style:{padding:"0 2px"},children:"▼"})})]}),e.jsxs(C,{className:I.menu,children:[e.jsx(t,{children:"Foo"}),e.jsx(t,{children:"Bar"}),e.jsx(t,{children:"Baz"}),e.jsx(t,{href:"http://google.com",children:"Google"})]})]})})})]})]})})})})]})}const r={render:()=>e.jsx(k,{}),parameters:{description:{data:'You should be able to click "Combobox Trigger" and then click on the textfield, closing the subdialog. A second click should move focus into the textfield'}}};o.__docgenInfo={description:"",methods:[],displayName:"ModalExample"};var c,x,m;o.parameters={...o.parameters,docs:{...(c=o.parameters)==null?void 0:c.docs,source:{originalSource:`() => <DialogTrigger>
    <Button>Open modal</Button>
    <ModalOverlay style={{
    position: 'fixed',
    zIndex: 100,
    top: 0,
    left: 0,
    bottom: 0,
    right: 0,
    background: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }}>
      <Modal style={{
      background: 'Canvas',
      color: 'CanvasText',
      border: '1px solid gray',
      padding: 30
    }}>
        <Dialog>
          {({
          close
        }) => <form style={{
          display: 'flex',
          flexDirection: 'column'
        }}>
              <Heading slot="title" style={{
            marginTop: 0
          }}>Sign up</Heading>
              <label>
                First Name: <input placeholder="John" />
              </label>
              <label>
                Last Name: <input placeholder="Smith" />
              </label>
              <Button onPress={close} style={{
            marginTop: 10
          }}>
                Submit
              </Button>
            </form>}
        </Dialog>
      </Modal>
    </ModalOverlay>
  </DialogTrigger>`,...(m=(x=o.parameters)==null?void 0:x.docs)==null?void 0:m.source}}};var p,g,h;r.parameters={...r.parameters,docs:{...(p=r.parameters)==null?void 0:p.docs,source:{originalSource:`{
  render: () => <InertTest />,
  parameters: {
    description: {
      data: 'You should be able to click "Combobox Trigger" and then click on the textfield, closing the subdialog. A second click should move focus into the textfield'
    }
  }
}`,...(h=(g=r.parameters)==null?void 0:g.docs)==null?void 0:h.source}}};const N=["ModalExample","InertTestStory"];export{r as InertTestStory,o as ModalExample,N as __namedExportsOrder,L as default};
