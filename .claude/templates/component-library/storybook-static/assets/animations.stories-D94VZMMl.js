import{j as a}from"./jsx-runtime-CDt2p4po.js";import{D as l,B as s,aw as t,ax as m,a4 as d,E as c}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const y={title:"React Aria Components - Animations"};let e={render:()=>a.jsx("div",{className:"App",children:a.jsxs(l,{children:[a.jsx(s,{children:"Open modal"}),a.jsx(t,{className:"my-overlay",children:a.jsx(m,{isDismissable:!0,className:"my-modal",children:a.jsx(d,{children:({close:i})=>a.jsxs(a.Fragment,{children:[a.jsx(c,{slot:"title",children:"Notice"}),a.jsx("p",{children:"This is a modal with a custom modal overlay."}),a.jsx(s,{onPress:i,children:"Close"})]})})})})]})})};var o,n,r;e.parameters={...e.parameters,docs:{...(o=e.parameters)==null?void 0:o.docs,source:{originalSource:`{
  render: (): React.ReactElement => {
    return <div className="App">
        <DialogTrigger>
          <Button>Open modal</Button>
          <ModalOverlay className="my-overlay">
            <Modal isDismissable className="my-modal">
              <Dialog>
                {({
                close
              }) => <>
                    <Heading slot="title">Notice</Heading>
                    <p>This is a modal with a custom modal overlay.</p>
                    <Button onPress={close}>Close</Button>
                  </>}
              </Dialog>
            </Modal>
          </ModalOverlay>
        </DialogTrigger>
      </div>;
  }
}`,...(r=(n=e.parameters)==null?void 0:n.docs)==null?void 0:r.source}}};const v=["ModalAnimation"];export{e as ModalAnimation,v as __namedExportsOrder,y as default};
