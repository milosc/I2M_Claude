import{j as e}from"./jsx-runtime-CDt2p4po.js";import{b1 as c,b0 as o,X as B,y as j,al as d,d as x,f as y,L as T,B as r,g as v,P as I,b as L}from"./Virtualizer-43kePMo2.js";import"./ColorSwatch-C5hr6lpG.js";import"./index-GiUgBvb1.js";import{c as i,a as t}from"./utils-N1pTmi3h.js";import{s as n}from"./index.module-B9nxguEg.js";/* empty css               */import"./index-C8NrMXaH.js";const A={title:"React Aria Components/Toolbar",component:c},a={args:{orientation:"horizontal"},render:s=>e.jsxs("div",{children:[e.jsx("label",{htmlFor:"before",children:"Input Before Toolbar"}),e.jsx("input",{id:"before",type:"text"}),e.jsxs(c,{...s,children:[e.jsxs("div",{role:"group","aria-label":"Text style",children:[e.jsx(o,{className:i(n,"toggleButtonExample"),children:e.jsx("strong",{children:"B"})}),e.jsx(o,{className:i(n,"toggleButtonExample"),children:e.jsx("div",{style:{textDecoration:"underline"},children:"U"})}),e.jsx(o,{className:i(n,"toggleButtonExample"),children:e.jsx("i",{children:"I"})})]}),e.jsxs(B,{children:[e.jsx("div",{className:"checkbox",children:e.jsx("svg",{viewBox:"0 0 18 18","aria-hidden":"true",children:e.jsx("polyline",{points:"1 9 7 14 15 4"})})}),"Night Mode"]}),e.jsx(j,{href:"https://google.com",children:"Help"})]}),e.jsx("label",{htmlFor:"after",children:"Input After Toolbar"}),e.jsx("input",{id:"after",type:"text"})]})},l={args:{orientation:"horizontal"},render:s=>e.jsxs(c,{...s,"aria-label":"Text formatting",children:[e.jsxs(d,{"aria-label":"Style",children:[e.jsx(o,{"aria-label":"Bold",children:e.jsx("b",{children:"B"})}),e.jsx(o,{"aria-label":"Italic",children:e.jsx("i",{children:"I"})}),e.jsx(o,{"aria-label":"Underline",children:e.jsx("u",{children:"U"})})]}),e.jsx(x,{orientation:"vertical"}),e.jsxs(y,{children:[e.jsx(T,{children:"Favorite Animal"}),e.jsxs(r,{children:[e.jsx(v,{}),e.jsx("span",{"aria-hidden":"true",children:"▼"})]}),e.jsx(I,{children:e.jsxs(L,{children:[e.jsx(t,{children:"Aardvark"}),e.jsx(t,{children:"Cat"}),e.jsx(t,{children:"Dog"}),e.jsx(t,{children:"Kangaroo"}),e.jsx(t,{children:"Panda"}),e.jsx(t,{children:"Snake"})]})})]}),e.jsx(x,{orientation:"vertical"}),e.jsxs(d,{"aria-label":"Clipboard",children:[e.jsx(r,{children:"Copy"}),e.jsx(r,{children:"Paste"}),e.jsx(r,{children:"Cut"})]})]})};var p,u,m;a.parameters={...a.parameters,docs:{...(p=a.parameters)==null?void 0:p.docs,source:{originalSource:`{
  args: {
    orientation: 'horizontal' as Orientation
  },
  render: (props: ToolbarProps) => {
    return <div>
        <label htmlFor="before">Input Before Toolbar</label>
        <input id="before" type="text" />
        <Toolbar {...props}>
          <div role="group" aria-label="Text style">
            <ToggleButton className={classNames(styles, 'toggleButtonExample')}><strong>B</strong></ToggleButton>
            <ToggleButton className={classNames(styles, 'toggleButtonExample')}><div style={{
              textDecoration: 'underline'
            }}>U</div></ToggleButton>
            <ToggleButton className={classNames(styles, 'toggleButtonExample')}><i>I</i></ToggleButton>
          </div>
          <Checkbox>
            <div className="checkbox">
              <svg viewBox="0 0 18 18" aria-hidden="true">
                <polyline points="1 9 7 14 15 4" />
              </svg>
            </div>
            Night Mode
          </Checkbox>
          <Link href="https://google.com">Help</Link>
        </Toolbar>
        <label htmlFor="after">Input After Toolbar</label>
        <input id="after" type="text" />
      </div>;
  }
}`,...(m=(u=a.parameters)==null?void 0:u.docs)==null?void 0:m.source}}};var g,h,b;l.parameters={...l.parameters,docs:{...(g=l.parameters)==null?void 0:g.docs,source:{originalSource:`{
  args: {
    orientation: 'horizontal' as Orientation
  },
  render: (props: ToolbarProps) => {
    return <Toolbar {...props} aria-label="Text formatting">
        <Group aria-label="Style">
          <ToggleButton aria-label="Bold">
            <b>B</b>
          </ToggleButton>
          <ToggleButton aria-label="Italic">
            <i>I</i>
          </ToggleButton>
          <ToggleButton aria-label="Underline">
            <u>U</u>
          </ToggleButton>
        </Group>
        <Separator orientation="vertical" />
        <Select>
          <Label>Favorite Animal</Label>
          <Button>
            <SelectValue />
            <span aria-hidden="true">▼</span>
          </Button>
          <Popover>
            <ListBox>
              <MyListBoxItem>Aardvark</MyListBoxItem>
              <MyListBoxItem>Cat</MyListBoxItem>
              <MyListBoxItem>Dog</MyListBoxItem>
              <MyListBoxItem>Kangaroo</MyListBoxItem>
              <MyListBoxItem>Panda</MyListBoxItem>
              <MyListBoxItem>Snake</MyListBoxItem>
            </ListBox>
          </Popover>
        </Select>
        <Separator orientation="vertical" />

        <Group aria-label="Clipboard">
          <Button>Copy</Button>
          <Button>Paste</Button>
          <Button>Cut</Button>
        </Group>
      </Toolbar>;
  }
}`,...(b=(h=l.parameters)==null?void 0:h.docs)==null?void 0:b.source}}};const F=["ToolbarExample","SelectSupport"];export{l as SelectSupport,a as ToolbarExample,F as __namedExportsOrder,A as default};
