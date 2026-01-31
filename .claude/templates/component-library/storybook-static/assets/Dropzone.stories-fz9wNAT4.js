import{j as e}from"./jsx-runtime-CDt2p4po.js";import{a as o}from"./index-B-lxVbXh.js";import{b7 as Y,b8 as t,aO as x,y as ee,B as E,a as f,b9 as oe,ba as re}from"./Virtualizer-43kePMo2.js";import{e as J,c as ne}from"./ColorSwatch-C5hr6lpG.js";import{R as z,r as se}from"./index-GiUgBvb1.js";import{$ as te}from"./useDrag-D4nPEkp-.js";import{c as b}from"./utils-N1pTmi3h.js";import{s as n}from"./index.module-B9nxguEg.js";/* empty css               */import"./v4-CtRu48qb.js";import"./index-C8NrMXaH.js";function K(r){let{children:s,focusClass:a,focusRingClass:p}=r,{isFocused:u,isFocusVisible:O,focusProps:X}=Y(r),y=z.Children.only(s);return z.cloneElement(y,J(y.props,{...X,className:ne({[a||""]:u,[p||""]:O})}))}const ue={title:"React Aria Components/Dropzone",component:t},i=r=>e.jsx("div",{children:e.jsx(t,{...r,"aria-label":"testing aria-label",className:n.dropzone,"data-testid":"drop-zone-example-with-file-trigger-link",onDrop:o("OnDrop"),onDropEnter:o("OnDropEnter"),onDropExit:o("OnDropExit"),children:e.jsx(x,{onSelect:o("onSelect"),children:e.jsx(ee,{children:"Upload"})})})}),l=r=>e.jsx("div",{children:e.jsx(t,{...r,className:n.dropzone,onDrop:o("OnDrop"),onDropEnter:o("OnDropEnter"),onDropExit:o("OnDropExit"),children:e.jsx(x,{onSelect:o("onSelect"),children:e.jsx(E,{children:"Upload"})})})}),c=r=>e.jsxs("div",{children:[e.jsx(j,{}),e.jsxs(t,{...r,className:n.dropzone,onDrop:o("OnDrop"),onDropEnter:o("OnDropEnter"),onDropExit:o("OnDropExit"),children:[e.jsx(x,{onSelect:o("onSelect"),children:e.jsx(E,{children:"Browse"})}),"Or drag into here"]})]}),d=r=>e.jsx("div",{children:e.jsx(t,{...r,getDropOperation:s=>s.has("image/png")?"copy":"cancel",className:n.dropzone,onDrop:o("OnDrop"),onDropEnter:o("OnDropEnter"),onDropExit:o("OnDropExit"),children:e.jsx(x,{onSelect:o("onSelect"),acceptedFileTypes:["image/png"],children:e.jsx(E,{children:"Upload"})})})}),D=r=>e.jsx("div",{children:e.jsx(t,{...r,getDropOperation:s=>s.has("image/png")?"copy":"cancel",className:n.dropzone,onDrop:o("OnDrop"),onDropEnter:o("OnDropEnter"),onDropExit:o("OnDropExit"),children:e.jsx(x,{onSelect:o("onSelect"),defaultCamera:"environment",children:e.jsx(E,{children:"Upload"})})})}),g=r=>e.jsxs("div",{children:[e.jsx(j,{}),e.jsx(t,{...r,className:n.dropzone,onDrop:o("OnDrop"),onDropEnter:o("OnDropEnter"),onDropExit:o("OnDropExit"),children:e.jsx(f,{slot:"label",children:"DropZone Area"})})]}),m=r=>e.jsxs("div",{children:[e.jsx(Q,{}),e.jsx(t,{...r,className:n.dropzone,onDrop:o("OnDrop"),onDropEnter:o("OnDropEnter"),onDropExit:o("OnDropExit"),children:e.jsx(f,{slot:"label",children:"DropZone Area"})})]}),ae=r=>e.jsxs("div",{children:[e.jsx(j,{}),e.jsx(Q,{}),e.jsx(t,{...r,className:n.dropzone,onPress:o("OnPress"),onDrop:o("OnDrop"),onDropEnter:o("OnDropEnter"),onDropExit:o("OnDropExit"),children:({isHovered:s,isFocused:a,isFocusVisible:p,isDropTarget:u,isDisabled:O})=>e.jsxs("div",{children:[e.jsx(f,{slot:"label",children:"DropzoneArea"}),e.jsxs("div",{children:["isHovered: ",s?"true":"false"]}),e.jsxs("div",{children:["isFocused: ",a?"true":"false"]}),e.jsxs("div",{children:["isFocusVisible: ",p?"true":"false"]}),e.jsxs("div",{children:["isDropTarget: ",u?"true":"false"]}),e.jsxs("div",{children:["isDisabled: ",O?"true":"false"]})]})})]}),h={args:{isDisabled:!1},argTypes:{isDisabled:{control:"boolean"}},render:r=>e.jsx(ae,{...r})},j=()=>{let r=se.useRef(null),{dragProps:s,isDragging:a}=te({getItems(){return[{"text/plain":"hello world"}]}}),{buttonProps:p}=oe({elementType:"div"},r);return e.jsx(K,{focusRingClass:b(n,"focus-ring"),children:e.jsx("div",{...J(p,s),ref:r,className:b(n,"draggable",{dragging:a}),children:"Drag me"})})},Q=()=>{let{clipboardProps:r}=re({getItems(){return[{"text/plain":"hello world"}]}});return e.jsx(K,{focusRingClass:b(n,"focus-ring"),children:e.jsx("div",{...r,role:"textbox","aria-label":"copyable element",tabIndex:0,className:n.copyable,children:"Copy me"})})};i.__docgenInfo={description:"",methods:[],displayName:"DropzoneExampleWithFileTriggerLink"};l.__docgenInfo={description:"",methods:[],displayName:"DropzoneExampleWithFileTriggerButton"};c.__docgenInfo={description:"",methods:[],displayName:"DropzoneExampleWithDraggableAndFileTrigger"};d.__docgenInfo={description:"",methods:[],displayName:"DropZoneOnlyAcceptPNGWithFileTrigger"};D.__docgenInfo={description:"",methods:[],displayName:"DropZoneWithCaptureMobileOnly"};g.__docgenInfo={description:"",methods:[],displayName:"DropzoneExampleWithDraggableObject"};m.__docgenInfo={description:"",methods:[],displayName:"DropzoneExampleWithCopyableObject"};var v,T,F;i.parameters={...i.parameters,docs:{...(v=i.parameters)==null?void 0:v.docs,source:{originalSource:`props => <div>
    <DropZone {...props} aria-label={'testing aria-label'} className={styles.dropzone} data-testid="drop-zone-example-with-file-trigger-link" onDrop={action('OnDrop')} onDropEnter={action('OnDropEnter')} onDropExit={action('OnDropExit')}>
      <FileTrigger onSelect={action('onSelect')}>
        <Link>Upload</Link>
      </FileTrigger>
    </DropZone>
  </div>`,...(F=(T=i.parameters)==null?void 0:T.docs)==null?void 0:F.source}}};var N,S,W;l.parameters={...l.parameters,docs:{...(N=l.parameters)==null?void 0:N.docs,source:{originalSource:`props => <div>
    <DropZone {...props} className={styles.dropzone} onDrop={action('OnDrop')} onDropEnter={action('OnDropEnter')} onDropExit={action('OnDropExit')}>
      <FileTrigger onSelect={action('onSelect')}>
        <Button>Upload</Button>
      </FileTrigger>
    </DropZone>
  </div>`,...(W=(S=l.parameters)==null?void 0:S.docs)==null?void 0:W.source}}};var Z,C,$;c.parameters={...c.parameters,docs:{...(Z=c.parameters)==null?void 0:Z.docs,source:{originalSource:`props => <div>
    <Draggable />
    <DropZone {...props} className={styles.dropzone} onDrop={action('OnDrop')} onDropEnter={action('OnDropEnter')} onDropExit={action('OnDropExit')}>
      <FileTrigger onSelect={action('onSelect')}>
        <Button>Browse</Button>
      </FileTrigger>
      Or drag into here
    </DropZone>
  </div>`,...($=(C=c.parameters)==null?void 0:C.docs)==null?void 0:$.source}}};var _,B,P;d.parameters={...d.parameters,docs:{...(_=d.parameters)==null?void 0:_.docs,source:{originalSource:`props => <div>
    <DropZone {...props} getDropOperation={types => types.has('image/png') ? 'copy' : 'cancel'} className={styles.dropzone} onDrop={action('OnDrop')} onDropEnter={action('OnDropEnter')} onDropExit={action('OnDropExit')}>
      <FileTrigger onSelect={action('onSelect')} acceptedFileTypes={['image/png']}>
        <Button>Upload</Button>
      </FileTrigger>
    </DropZone>
  </div>`,...(P=(B=d.parameters)==null?void 0:B.docs)==null?void 0:P.source}}};var R,A,I;D.parameters={...D.parameters,docs:{...(R=D.parameters)==null?void 0:R.docs,source:{originalSource:`props => <div>
    <DropZone {...props} getDropOperation={types => types.has('image/png') ? 'copy' : 'cancel'} className={styles.dropzone} onDrop={action('OnDrop')} onDropEnter={action('OnDropEnter')} onDropExit={action('OnDropExit')}>
      <FileTrigger onSelect={action('onSelect')} defaultCamera="environment">
        <Button>Upload</Button>
      </FileTrigger>
    </DropZone>
  </div>`,...(I=(A=D.parameters)==null?void 0:A.docs)==null?void 0:I.source}}};var k,U,w;g.parameters={...g.parameters,docs:{...(k=g.parameters)==null?void 0:k.docs,source:{originalSource:`props => <div>
    <Draggable />
    <DropZone {...props} className={styles.dropzone} onDrop={action('OnDrop')} onDropEnter={action('OnDropEnter')} onDropExit={action('OnDropExit')}>
      <Text slot="label">
        DropZone Area
      </Text>
    </DropZone>
  </div>`,...(w=(U=g.parameters)==null?void 0:U.docs)==null?void 0:w.source}}};var L,G,M;m.parameters={...m.parameters,docs:{...(L=m.parameters)==null?void 0:L.docs,source:{originalSource:`props => <div>
    <Copyable />
    <DropZone {...props} className={styles.dropzone} onDrop={action('OnDrop')} onDropEnter={action('OnDropEnter')} onDropExit={action('OnDropExit')}>
      <Text slot="label">
        DropZone Area
      </Text>
    </DropZone>
  </div>`,...(M=(G=m.parameters)==null?void 0:G.docs)==null?void 0:M.source}}};var V,H,q;h.parameters={...h.parameters,docs:{...(V=h.parameters)==null?void 0:V.docs,source:{originalSource:`{
  args: {
    isDisabled: false
  },
  argTypes: {
    isDisabled: {
      control: 'boolean'
    }
  },
  render: args => <DropzoneWithRenderPropsExample {...args} />
}`,...(q=(H=h.parameters)==null?void 0:H.docs)==null?void 0:q.source}}};const Oe=["DropzoneExampleWithFileTriggerLink","DropzoneExampleWithFileTriggerButton","DropzoneExampleWithDraggableAndFileTrigger","DropZoneOnlyAcceptPNGWithFileTrigger","DropZoneWithCaptureMobileOnly","DropzoneExampleWithDraggableObject","DropzoneExampleWithCopyableObject","DropzoneWithRenderProps"];export{d as DropZoneOnlyAcceptPNGWithFileTrigger,D as DropZoneWithCaptureMobileOnly,m as DropzoneExampleWithCopyableObject,c as DropzoneExampleWithDraggableAndFileTrigger,g as DropzoneExampleWithDraggableObject,l as DropzoneExampleWithFileTriggerButton,i as DropzoneExampleWithFileTriggerLink,h as DropzoneWithRenderProps,Oe as __namedExportsOrder,ue as default};
