import{j as e}from"./jsx-runtime-CDt2p4po.js";import{a as M}from"./index-B-lxVbXh.js";import{o as n,L as f,p as l,q as v,r as b,O as j,au as C,B as s}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";/* empty css               */import"./v4-CtRu48qb.js";import"./index-C8NrMXaH.js";const N={title:"React Aria Components/TagGroup",component:n,args:{selectionMode:"none",selectionBehavior:"toggle"},argTypes:{selectionMode:{control:"inline-radio",options:["none","single","multiple"]},selectionBehavior:{control:"inline-radio",options:["toggle","replace"]}},excludeStories:["MyTag"]},t={render:o=>e.jsxs(n,{...o,children:[e.jsx(f,{children:"Categories"}),e.jsxs(l,{style:{display:"flex",gap:4},children:[e.jsx(r,{href:"https://nytimes.com",children:"News"}),e.jsx(r,{children:"Travel"}),e.jsx(r,{children:"Gaming"}),e.jsxs(v,{children:[e.jsx(r,{children:"Shopping"}),e.jsxs(b,{offset:5,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:5,borderRadius:4},children:[e.jsx(j,{style:{transform:"translateX(-50%)"},children:e.jsx("svg",{width:"8",height:"8",style:{display:"block"},children:e.jsx("path",{d:"M0 0L4 4L8 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),"I am a tooltip"]})]})]})]})};function r(o){return e.jsx(C,{...o,style:({isSelected:d})=>({border:"1px solid gray",borderRadius:4,padding:"0 4px",background:d?"black":"",color:d?"white":"",cursor:o.href?"pointer":"default"})})}const a={render:o=>e.jsxs(n,{...o,onRemove:M("onRemove"),children:[e.jsx(f,{children:"Categories"}),e.jsxs(l,{style:{display:"flex",gap:4},children:[e.jsxs(r,{children:["Marsupial",e.jsx(s,{slot:"remove",children:"X"})]}),e.jsxs(r,{children:["Animal",e.jsx(s,{slot:"remove",children:"X"})]}),e.jsxs(r,{children:["Mammal",e.jsx(s,{slot:"remove",children:"X"})]}),e.jsxs(v,{children:[e.jsxs(r,{children:["Chordate",e.jsx(s,{slot:"remove",children:"X"})]}),e.jsxs(b,{offset:5,style:{background:"Canvas",color:"CanvasText",border:"1px solid gray",padding:5,borderRadius:4},children:[e.jsx(j,{style:{transform:"translateX(-50%)"},children:e.jsx("svg",{width:"8",height:"8",style:{display:"block"},children:e.jsx("path",{d:"M0 0L4 4L8 0",fill:"white",strokeWidth:1,stroke:"gray"})})}),"I am a tooltip"]})]})]})]})},i={render:o=>e.jsx(n,{...o,"aria-label":"Categories",children:e.jsx(l,{renderEmptyState:()=>"No categories.",children:[]})})};r.__docgenInfo={description:"",methods:[],displayName:"MyTag",props:{className:{required:!1,tsType:{name:"union",raw:"string | ((values: T & {defaultClassName: string | undefined}) => string)",elements:[{name:"string"},{name:"unknown"}]},description:"The CSS [className](https://developer.mozilla.org/en-US/docs/Web/API/Element/className) for the element. A function may be provided to compute the class based on component state."},style:{required:!1,tsType:{name:"union",raw:"CSSProperties | ((values: T & {defaultStyle: CSSProperties}) => CSSProperties | undefined)",elements:[{name:"CSSProperties"},{name:"unknown"}]},description:"The inline [style](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style) for the element. A function may be provided to compute the style based on component state."},children:{required:!1,tsType:{name:"union",raw:"ReactNode | ((values: T & {defaultChildren: ReactNode | undefined}) => ReactNode)",elements:[{name:"ReactNode"},{name:"unknown"}]},description:"The children of the component. A function may be provided to alter the children based on component state."},id:{required:!1,tsType:{name:"Key"},description:"A unique id for the tag."},textValue:{required:!1,tsType:{name:"string"},description:`A string representation of the tags's contents, used for accessibility.
Required if children is not a plain text string.`},isDisabled:{required:!1,tsType:{name:"boolean"},description:"Whether the tag is disabled."}},composes:["LinkDOMProps","HoverEvents","PressEvents","Omit"]};var p,g,c;t.parameters={...t.parameters,docs:{...(p=t.parameters)==null?void 0:p.docs,source:{originalSource:`{
  render: (props: TagGroupProps) => <TagGroup {...props}>
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
}`,...(c=(g=t.parameters)==null?void 0:g.docs)==null?void 0:c.source}}};var m,h,u;a.parameters={...a.parameters,docs:{...(m=a.parameters)==null?void 0:m.docs,source:{originalSource:`{
  render: (props: TagGroupProps) => <TagGroup {...props} onRemove={action('onRemove')}>
      <Label>Categories</Label>
      <TagList style={{
      display: 'flex',
      gap: 4
    }}>
        <MyTag>Marsupial<Button slot="remove">X</Button></MyTag>
        <MyTag>Animal<Button slot="remove">X</Button></MyTag>
        <MyTag>Mammal<Button slot="remove">X</Button></MyTag>
        <TooltipTrigger>
          <MyTag>Chordate<Button slot="remove">X</Button></MyTag>
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
}`,...(u=(h=a.parameters)==null?void 0:h.docs)==null?void 0:u.source}}};var y,T,x;i.parameters={...i.parameters,docs:{...(y=i.parameters)==null?void 0:y.docs,source:{originalSource:`{
  render: (props: TagGroupProps) => <TagGroup {...props} aria-label="Categories">
      <TagList renderEmptyState={() => 'No categories.'}>
        {[]}
      </TagList>
    </TagGroup>
}`,...(x=(T=i.parameters)==null?void 0:T.docs)==null?void 0:x.source}}};const B=["TagGroupExample","MyTag","TagGroupExampleWithRemove","EmptyTagGroup"];export{i as EmptyTagGroup,r as MyTag,t as TagGroupExample,a as TagGroupExampleWithRemove,B as __namedExportsOrder,N as default};
