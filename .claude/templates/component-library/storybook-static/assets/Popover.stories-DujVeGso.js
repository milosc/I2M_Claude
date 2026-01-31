import{j as e}from"./jsx-runtime-CDt2p4po.js";import{P as o,D as s,B as r,O as l,a4 as i,E as I}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import{r as p}from"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const q={title:"React Aria Components/Popover",component:o,args:{placement:"bottom start",hideArrow:!1},argTypes:{placement:{control:"select",options:["bottom","bottom left","bottom right","bottom start","bottom end","top","top left","top right","top start","top end","left","left top","left bottom","start","start top","start bottom","right","right top","right bottom","end","end top","end bottom"]},animation:{control:"radio",options:["transition","animation","animation-delayed"]}}},h=t=>e.jsxs(s,{children:[e.jsx(r,{children:"Open popover"}),e.jsxs(o,{...t,className:({isEntering:n,isExiting:a})=>`popover-base ${t.animation||""} ${n?"entering":""} ${a?"exiting":""}`,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:30,zIndex:5},children:[!t.hideArrow&&e.jsx(l,{style:{display:"flex"},children:e.jsx("svg",{width:"12",height:"12",viewBox:"0 0 12 12",style:{display:"block"},children:e.jsx("path",{d:"M0 0L6 6L12 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),e.jsx(i,{children:({close:n})=>e.jsxs("form",{style:{display:"flex",flexDirection:"column"},children:[e.jsx(I,{slot:"title",children:"Sign up"}),e.jsxs("label",{children:["First Name: ",e.jsx("input",{placeholder:"John"})]}),e.jsxs("label",{children:["Last Name: ",e.jsx("input",{placeholder:"Smith"})]}),e.jsx(r,{onPress:n,style:{marginTop:10},children:"Submit"})]})})]})]}),y=5e3;function A(){const t=p.useRef(null),[n,a]=p.useState(y);return p.useEffect(()=>{if(n>0){const d=setInterval(()=>{a(n-1e3)},1e3);return()=>{clearInterval(d)}}},[n]),p.useEffect(()=>{const d=setTimeout(()=>{t.current&&(t.current.style.width="200px",t.current.style.height="50px")},y+1e3);return()=>{clearTimeout(d)}},[]),e.jsxs("div",{style:{marginBottom:100,display:"flex",flexDirection:"column",alignItems:"center"},children:[e.jsx("div",{children:e.jsxs("p",{children:["The trigger button below will change size in ",e.jsxs("strong",{children:[Math.floor(n/1e3),"s"]})]})}),e.jsxs(s,{defaultOpen:!0,children:[e.jsx(r,{ref:t,children:"Open popover"}),e.jsx(o,{placement:"bottom start",style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:30,zIndex:5},children:e.jsx(i,{children:({close:d})=>e.jsxs("form",{style:{display:"flex",flexDirection:"column"},children:[e.jsx(I,{slot:"title",children:"Sign up"}),e.jsxs("label",{children:["First Name: ",e.jsx("input",{placeholder:"John"})]}),e.jsxs("label",{children:["Last Name: ",e.jsx("input",{placeholder:"Smith"})]}),e.jsx(r,{onPress:d,style:{marginTop:10},children:"Submit"})]})})})]})]})}const x={render:()=>e.jsx(A,{})};function N({topLeft:t,topRight:n,leftTop:a,leftBottom:d,rightTop:S,rightBottom:D,bottomLeft:z,bottomRight:W}){return e.jsxs("div",{style:{display:"flex",flexDirection:"column"},children:[e.jsxs("div",{style:{display:"flex"},children:[e.jsx("div",{style:{padding:12},children:e.jsxs(s,{children:[e.jsx(r,{style:{width:200,height:100},children:"Top left"}),e.jsxs(o,{placement:"top left",shouldFlip:!1,arrowBoundaryOffset:t,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:8,zIndex:5,borderRadius:"30px"},children:[e.jsx(l,{style:{display:"flex"},children:e.jsx("svg",{width:"12",height:"12",viewBox:"0 0 12 12",style:{display:"block"},children:e.jsx("path",{d:"M0 0L6 6L12 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),e.jsx(i,{style:{outline:"none"},children:e.jsx("div",{children:"Top left"})})]})]})}),e.jsx("div",{style:{padding:12},children:e.jsxs(s,{children:[e.jsx(r,{style:{width:200,height:100},children:"Top right"}),e.jsxs(o,{placement:"top right",shouldFlip:!1,arrowBoundaryOffset:n,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:8,zIndex:5,borderRadius:"30px"},children:[e.jsx(l,{style:{display:"flex"},children:e.jsx("svg",{width:"12",height:"12",viewBox:"0 0 12 12",style:{display:"block"},children:e.jsx("path",{d:"M0 0L6 6L12 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),e.jsx(i,{style:{outline:"none"},children:e.jsx("div",{children:"Top right"})})]})]})})]}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx("div",{style:{padding:12},children:e.jsxs(s,{children:[e.jsx(r,{style:{width:200,height:100},children:"Left top"}),e.jsxs(o,{placement:"left top",shouldFlip:!1,arrowBoundaryOffset:a,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:8,zIndex:5,borderRadius:"30px"},children:[e.jsx(l,{style:{display:"flex"},children:e.jsx("svg",{width:"12",height:"12",viewBox:"0 0 12 12",style:{display:"block",transform:"rotate(-90deg)"},children:e.jsx("path",{d:"M0 0L6 6L12 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),e.jsx(i,{style:{outline:"none"},children:e.jsx("div",{children:"Left top"})})]})]})}),e.jsx("div",{style:{padding:12},children:e.jsxs(s,{children:[e.jsx(r,{style:{width:200,height:100},children:"Left bottom"}),e.jsxs(o,{placement:"left bottom",shouldFlip:!1,arrowBoundaryOffset:d,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:8,zIndex:5,borderRadius:"30px"},children:[e.jsx(l,{style:{display:"flex"},children:e.jsx("svg",{width:"12",height:"12",viewBox:"0 0 12 12",style:{display:"block",transform:"rotate(-90deg)"},children:e.jsx("path",{d:"M0 0L6 6L12 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),e.jsx(i,{style:{outline:"none"},children:e.jsx("div",{children:"Left bottom"})})]})]})})]}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx("div",{style:{padding:12},children:e.jsxs(s,{children:[e.jsx(r,{style:{width:200,height:100},children:"Right top"}),e.jsxs(o,{placement:"right top",shouldFlip:!1,arrowBoundaryOffset:S,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:8,zIndex:5,borderRadius:"30px"},children:[e.jsx(l,{style:{display:"flex"},children:e.jsx("svg",{width:"12",height:"12",viewBox:"0 0 12 12",style:{display:"block",transform:"rotate(90deg)"},children:e.jsx("path",{d:"M0 0L6 6L12 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),e.jsx(i,{style:{outline:"none"},children:e.jsx("div",{children:"Right top"})})]})]})}),e.jsx("div",{style:{padding:12},children:e.jsxs(s,{children:[e.jsx(r,{style:{width:200,height:100},children:"Right bottom"}),e.jsxs(o,{placement:"right bottom",shouldFlip:!1,arrowBoundaryOffset:D,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:8,zIndex:5,borderRadius:"30px"},children:[e.jsx(l,{style:{display:"flex"},children:e.jsx("svg",{width:"12",height:"12",viewBox:"0 0 12 12",style:{display:"block",transform:"rotate(90deg)"},children:e.jsx("path",{d:"M0 0L6 6L12 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),e.jsx(i,{style:{outline:"none"},children:e.jsx("div",{children:"Right bottom"})})]})]})})]}),e.jsxs("div",{style:{display:"flex"},children:[e.jsx("div",{style:{padding:12},children:e.jsxs(s,{children:[e.jsx(r,{style:{width:200,height:100},children:"Bottom left"}),e.jsxs(o,{placement:"bottom left",shouldFlip:!1,arrowBoundaryOffset:z,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:8,zIndex:5,borderRadius:"30px"},children:[e.jsx(l,{style:{display:"flex"},children:e.jsx("svg",{width:"12",height:"12",viewBox:"0 0 12 12",style:{display:"block",transform:"rotate(180deg)"},children:e.jsx("path",{d:"M0 0L6 6L12 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),e.jsx(i,{style:{outline:"none"},children:e.jsx("div",{children:"Bottom left"})})]})]})}),e.jsx("div",{style:{padding:12},children:e.jsxs(s,{children:[e.jsx(r,{style:{width:200,height:100},children:"Bottom right"}),e.jsxs(o,{placement:"bottom right",shouldFlip:!1,arrowBoundaryOffset:W,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:8,zIndex:5,borderRadius:"30px"},children:[e.jsx(l,{style:{display:"flex"},children:e.jsx("svg",{width:"12",height:"12",viewBox:"0 0 12 12",style:{display:"block",transform:"rotate(180deg)"},children:e.jsx("path",{d:"M0 0L6 6L12 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),e.jsx(i,{style:{outline:"none"},children:e.jsx("div",{children:"Bottom right"})})]})]})})]})]})}const g={args:{topLeft:25,topRight:25,leftTop:15,leftBottom:15,rightTop:15,rightBottom:15,bottomLeft:25,bottomRight:25},argTypes:{topLeft:{control:{type:"range",min:-100,max:100}},topRight:{control:{type:"range",min:-100,max:100}},leftTop:{control:{type:"range",min:-100,max:100}},leftBottom:{control:{type:"range",min:-100,max:100}},rightTop:{control:{type:"range",min:-100,max:100}},rightBottom:{control:{type:"range",min:-100,max:100}},bottomLeft:{control:{type:"range",min:-100,max:100}},bottomRight:{control:{type:"range",min:-100,max:100}}},render:t=>e.jsx(N,{...t})},c=()=>e.jsxs(s,{children:[e.jsx(r,{children:"Open popover"}),e.jsx(o,{placement:"bottom start",style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",zIndex:5,width:"var(--trigger-width)"},children:e.jsx(i,{children:"Should match the width of the trigger button"})})]});function F(t){let[n,a]=p.useState(null);return e.jsx("div",{id:"scrolling-boundary",ref:a,style:{height:300,width:300,overflow:"auto",border:"1px solid light-dark(black, white)"},children:e.jsx("div",{style:{width:600,height:600,display:"flex",alignItems:"center",justifyContent:"center"},children:e.jsxs(s,{children:[e.jsx(r,{style:{width:200,height:200,display:"flex",alignItems:"center",justifyContent:"center"},children:"Open popover"}),e.jsx(o,{...t,boundaryElement:n??void 0,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",zIndex:5},children:e.jsx(i,{children:"This is some dummy content for the popover"})})]})})})}const m={render:t=>e.jsx(F,{...t}),args:{containerPadding:0,placement:"bottom"},argTypes:{containerPadding:{control:{type:"range",min:0,max:100}},hideArrow:{table:{disable:!0}},animation:{table:{disable:!0}}}};h.__docgenInfo={description:"",methods:[],displayName:"PopoverExample"};c.__docgenInfo={description:"",methods:[],displayName:"PopoverTriggerWidthExample"};var f,u,j;h.parameters={...h.parameters,docs:{...(f=h.parameters)==null?void 0:f.docs,source:{originalSource:`args => <DialogTrigger>
    <Button>Open popover</Button>
    <Popover {...args} className={({
    isEntering,
    isExiting
  }) => \`popover-base \${(args as any).animation || ''} \${isEntering ? 'entering' : ''} \${isExiting ? 'exiting' : ''}\`} style={{
    background: 'Canvas',
    color: 'CanvasText',
    border: '1px solid gray',
    padding: 30,
    zIndex: 5
  }}>
      {!(args as any).hideArrow && <OverlayArrow style={{
      display: 'flex'
    }}>
        <svg width="12" height="12" viewBox="0 0 12 12" style={{
        display: 'block'
      }}>
          <path d="M0 0L6 6L12 0" fill="white" strokeWidth={1} stroke="gray" />
        </svg>
      </OverlayArrow>}
      <Dialog>
        {({
        close
      }) => <form style={{
        display: 'flex',
        flexDirection: 'column'
      }}>
            <Heading slot="title">Sign up</Heading>
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
    </Popover>
  </DialogTrigger>`,...(j=(u=h.parameters)==null?void 0:u.docs)==null?void 0:j.source}}};var v,b,w;x.parameters={...x.parameters,docs:{...(v=x.parameters)==null?void 0:v.docs,source:{originalSource:`{
  render: () => <PopoverTriggerObserver />
}`,...(w=(b=x.parameters)==null?void 0:b.docs)==null?void 0:w.source}}};var T,B,k;g.parameters={...g.parameters,docs:{...(T=g.parameters)==null?void 0:T.docs,source:{originalSource:`{
  args: {
    topLeft: 25,
    topRight: 25,
    leftTop: 15,
    leftBottom: 15,
    rightTop: 15,
    rightBottom: 15,
    bottomLeft: 25,
    bottomRight: 25
  },
  argTypes: {
    topLeft: {
      control: {
        type: 'range',
        min: -100,
        max: 100
      }
    },
    topRight: {
      control: {
        type: 'range',
        min: -100,
        max: 100
      }
    },
    leftTop: {
      control: {
        type: 'range',
        min: -100,
        max: 100
      }
    },
    leftBottom: {
      control: {
        type: 'range',
        min: -100,
        max: 100
      }
    },
    rightTop: {
      control: {
        type: 'range',
        min: -100,
        max: 100
      }
    },
    rightBottom: {
      control: {
        type: 'range',
        min: -100,
        max: 100
      }
    },
    bottomLeft: {
      control: {
        type: 'range',
        min: -100,
        max: 100
      }
    },
    bottomRight: {
      control: {
        type: 'range',
        min: -100,
        max: 100
      }
    }
  },
  render: args => <PopoverArrowBoundaryOffsetExampleRender {...args} />
}`,...(k=(B=g.parameters)==null?void 0:B.docs)==null?void 0:k.source}}};var C,L,O;c.parameters={...c.parameters,docs:{...(C=c.parameters)==null?void 0:C.docs,source:{originalSource:`() => <DialogTrigger>
    <Button>Open popover</Button>
    <Popover placement="bottom start" style={{
    background: 'Canvas',
    color: 'CanvasText',
    border: '1px solid gray',
    zIndex: 5,
    width: 'var(--trigger-width)'
  }}>
      <Dialog>
        Should match the width of the trigger button
      </Dialog>
    </Popover>
  </DialogTrigger>`,...(O=(L=c.parameters)==null?void 0:L.docs)==null?void 0:O.source}}};var P,E,R;m.parameters={...m.parameters,docs:{...(P=m.parameters)==null?void 0:P.docs,source:{originalSource:`{
  render: args => <ScrollingBoundaryContainerExample {...args} />,
  args: {
    containerPadding: 0,
    placement: 'bottom'
  },
  argTypes: {
    containerPadding: {
      control: {
        type: 'range',
        min: 0,
        max: 100
      }
    },
    hideArrow: {
      table: {
        disable: true
      }
    },
    animation: {
      table: {
        disable: true
      }
    }
  }
}`,...(R=(E=m.parameters)==null?void 0:E.docs)==null?void 0:R.source}}};const G=["PopoverExample","PopoverTriggerObserverExample","PopoverArrowBoundaryOffsetExample","PopoverTriggerWidthExample","ScrollingBoundaryContainer"];export{g as PopoverArrowBoundaryOffsetExample,h as PopoverExample,x as PopoverTriggerObserverExample,c as PopoverTriggerWidthExample,m as ScrollingBoundaryContainer,G as __namedExportsOrder,q as default};
