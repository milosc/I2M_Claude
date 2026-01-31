import{j as e}from"./jsx-runtime-CDt2p4po.js";import{z as x,B as n,E as c,F as a,J as d,N as H,Q as C,U as T,W as V}from"./Virtualizer-43kePMo2.js";import{$ as P}from"./ColorSwatch-C5hr6lpG.js";import{r as W,R as _}from"./index-GiUgBvb1.js";/* empty css               */import"./index-C8NrMXaH.js";const Y={title:"React Aria Components/Calendar",component:x};function N(){const s=W.useContext(T),t=s==null?void 0:s.setValue;return e.jsx("div",{children:e.jsx(n,{slot:null,className:"reset-button",onPress:()=>{t==null||t(null)},children:"Reset value"})})}const g={render:()=>e.jsxs(x,{style:{width:220},children:[e.jsxs("div",{style:{display:"flex",alignItems:"center"},children:[e.jsx(n,{slot:"previous",children:"<"}),e.jsx(c,{style:{flex:1,textAlign:"center"}}),e.jsx(n,{slot:"next",children:">"})]}),e.jsx(a,{style:{width:"100%"},children:s=>e.jsx(d,{date:s,style:({isSelected:t,isOutsideMonth:l})=>({display:l?"none":"",textAlign:"center",cursor:"default",background:t?"blue":""})})})]})},p={render:()=>e.jsxs(x,{style:{width:220},children:[e.jsxs("div",{style:{display:"flex",alignItems:"center"},children:[e.jsx(n,{slot:"previous",children:"<"}),e.jsx(c,{style:{flex:1,textAlign:"center"}}),e.jsx(n,{slot:"next",children:">"})]}),e.jsx(a,{style:{width:"100%"},children:s=>e.jsx(d,{date:s,style:({isSelected:t,isOutsideMonth:l})=>({display:l?"none":"",textAlign:"center",cursor:"default",background:t?"blue":""})})}),e.jsx(N,{})]})};function z(s){let t=new V(2021,7,1),[l,r]=_.useState(t);return e.jsxs(e.Fragment,{children:[e.jsx("button",{style:{marginBottom:20},onClick:()=>r(t),children:"Reset focused date"}),e.jsxs(x,{style:{width:500},visibleDuration:{months:3},focusedValue:l,onFocusChange:r,defaultValue:t,...s,children:[e.jsxs("div",{style:{display:"flex",alignItems:"center"},children:[e.jsx(n,{slot:"previous",children:"<"}),e.jsx(c,{style:{flex:1,textAlign:"center"}}),e.jsx(n,{slot:"next",children:">"})]}),e.jsxs("div",{style:{display:"flex",gap:20},children:[e.jsx(a,{style:{flex:1},children:o=>e.jsx(d,{date:o,style:({isSelected:u,isOutsideMonth:i})=>({opacity:i?"0.5":"",textAlign:"center",cursor:"default",background:u&&!i?"blue":""})})}),e.jsx(a,{style:{flex:1},offset:{months:1},children:o=>e.jsx(d,{date:o,style:({isSelected:u,isOutsideMonth:i})=>({opacity:i?"0.5":"",textAlign:"center",cursor:"default",background:u&&!i?"blue":""})})}),e.jsx(a,{style:{flex:1},offset:{months:2},children:o=>e.jsx(d,{date:o,style:({isSelected:u,isOutsideMonth:i})=>({opacity:i?"0.5":"",textAlign:"center",cursor:"default",background:u&&!i?"blue":""})})})]})]})]})}const y={render:s=>e.jsx(z,{...s}),args:{selectionAlignment:"center"},argTypes:{selectionAlignment:{control:"select",options:["start","center","end"]}}},f={render:function(t){return e.jsx("div",{children:e.jsx(P,{locale:t.locale,children:e.jsxs(x,{style:{width:220},children:[e.jsxs("div",{style:{display:"flex",alignItems:"center"},children:[e.jsx(n,{slot:"previous",children:"<"}),e.jsx(c,{style:{flex:1,textAlign:"center"}}),e.jsx(n,{slot:"next",children:">"})]}),e.jsx(a,{style:{width:"100%"},children:l=>e.jsx(d,{date:l,style:({isSelected:r,isOutsideMonth:o})=>({display:o?"none":"",textAlign:"center",cursor:"default",background:r?"blue":""})})})]})})})},args:{locale:"en-US-u-ca-iso8601-fw-tue"},argTypes:{locale:{control:"select",options:["en-US-u-ca-iso8601-fw-tue","en-US-u-ca-iso8601","en-US","fr-FR-u-ca-iso8601-fw-tue","fr-FR-u-ca-iso8601","fr-FR","en-US-u-ca-iso8601-fw-tue-nu-thai"]}}},h={render:()=>e.jsxs(H,{style:{width:220},children:[e.jsxs("div",{style:{display:"flex",alignItems:"center"},children:[e.jsx(n,{slot:"previous",children:"<"}),e.jsx(c,{style:{flex:1,textAlign:"center"}}),e.jsx(n,{slot:"next",children:">"})]}),e.jsx(a,{style:{width:"100%"},children:s=>e.jsx(d,{date:s,style:({isSelected:t,isOutsideMonth:l})=>({display:l?"none":"",textAlign:"center",cursor:"default",background:t?"blue":""})})})]})},m={render:s=>e.jsxs(H,{style:{width:500},visibleDuration:{months:3},defaultValue:{start:C("2025-08-04"),end:C("2025-08-10")},...s,children:[e.jsxs("div",{style:{display:"flex",alignItems:"center"},children:[e.jsx(n,{slot:"previous",children:"<"}),e.jsx(c,{style:{flex:1,textAlign:"center"}}),e.jsx(n,{slot:"next",children:">"})]}),e.jsxs("div",{style:{display:"flex",gap:20},children:[e.jsx(a,{style:{flex:1},children:t=>e.jsx(d,{date:t,style:({isSelected:l,isOutsideMonth:r})=>({display:r?"none":"",textAlign:"center",cursor:"default",background:l?"blue":""})})}),e.jsx(a,{style:{flex:1},offset:{months:1},children:t=>e.jsx(d,{date:t,style:({isSelected:l,isOutsideMonth:r})=>({display:r?"none":"",textAlign:"center",cursor:"default",background:l?"blue":""})})}),e.jsx(a,{style:{flex:1},offset:{months:2},children:t=>e.jsx(d,{date:t,style:({isSelected:l,isOutsideMonth:r})=>({display:r?"none":"",textAlign:"center",cursor:"default",background:l?"blue":""})})})]})]}),args:{selectionAlignment:"center"},argTypes:{selectionAlignment:{control:"select",options:["start","center","end"]}}};var j,b,v;g.parameters={...g.parameters,docs:{...(j=g.parameters)==null?void 0:j.docs,source:{originalSource:`{
  render: () => <Calendar style={{
    width: 220
  }}>
      <div style={{
      display: 'flex',
      alignItems: 'center'
    }}>
        <Button slot="previous">&lt;</Button>
        <Heading style={{
        flex: 1,
        textAlign: 'center'
      }} />
        <Button slot="next">&gt;</Button>
      </div>
      <CalendarGrid style={{
      width: '100%'
    }}>
        {date => <CalendarCell date={date} style={({
        isSelected,
        isOutsideMonth
      }) => ({
        display: isOutsideMonth ? 'none' : '',
        textAlign: 'center',
        cursor: 'default',
        background: isSelected ? 'blue' : ''
      })} />}
      </CalendarGrid>
    </Calendar>
}`,...(v=(b=g.parameters)==null?void 0:b.docs)==null?void 0:v.source}}};var A,S,w;p.parameters={...p.parameters,docs:{...(A=p.parameters)==null?void 0:A.docs,source:{originalSource:`{
  render: () => <Calendar style={{
    width: 220
  }}>
      <div style={{
      display: 'flex',
      alignItems: 'center'
    }}>
        <Button slot="previous">&lt;</Button>
        <Heading style={{
        flex: 1,
        textAlign: 'center'
      }} />
        <Button slot="next">&gt;</Button>
      </div>
      <CalendarGrid style={{
      width: '100%'
    }}>
        {date => <CalendarCell date={date} style={({
        isSelected,
        isOutsideMonth
      }) => ({
        display: isOutsideMonth ? 'none' : '',
        textAlign: 'center',
        cursor: 'default',
        background: isSelected ? 'blue' : ''
      })} />}
      </CalendarGrid>
      <Footer />
    </Calendar>
}`,...(w=(S=p.parameters)==null?void 0:S.docs)==null?void 0:w.source}}};var B,M,R;y.parameters={...y.parameters,docs:{...(B=y.parameters)==null?void 0:B.docs,source:{originalSource:`{
  render: args => <CalendarMultiMonthExample {...args} />,
  args: {
    selectionAlignment: 'center'
  },
  argTypes: {
    selectionAlignment: {
      control: 'select',
      options: ['start', 'center', 'end']
    }
  }
}`,...(R=(M=y.parameters)==null?void 0:M.docs)==null?void 0:R.source}}};var k,E,G;f.parameters={...f.parameters,docs:{...(k=f.parameters)==null?void 0:k.docs,source:{originalSource:`{
  render: function Example(args) {
    return <div>
        <I18nProvider locale={args.locale}>
          <Calendar style={{
          width: 220
        }}>
            <div style={{
            display: 'flex',
            alignItems: 'center'
          }}>
              <Button slot="previous">&lt;</Button>
              <Heading style={{
              flex: 1,
              textAlign: 'center'
            }} />
              <Button slot="next">&gt;</Button>
            </div>
            <CalendarGrid style={{
            width: '100%'
          }}>
              {date => <CalendarCell date={date} style={({
              isSelected,
              isOutsideMonth
            }) => ({
              display: isOutsideMonth ? 'none' : '',
              textAlign: 'center',
              cursor: 'default',
              background: isSelected ? 'blue' : ''
            })} />}
            </CalendarGrid>
          </Calendar>
        </I18nProvider>
      </div>;
  },
  args: {
    locale: 'en-US-u-ca-iso8601-fw-tue'
  },
  argTypes: {
    locale: {
      control: 'select',
      options: ['en-US-u-ca-iso8601-fw-tue', 'en-US-u-ca-iso8601', 'en-US', 'fr-FR-u-ca-iso8601-fw-tue', 'fr-FR-u-ca-iso8601', 'fr-FR', 'en-US-u-ca-iso8601-fw-tue-nu-thai']
    }
  }
}`,...(G=(E=f.parameters)==null?void 0:E.docs)==null?void 0:G.source}}};var F,O,I;h.parameters={...h.parameters,docs:{...(F=h.parameters)==null?void 0:F.docs,source:{originalSource:`{
  render: () => <RangeCalendar style={{
    width: 220
  }}>
      <div style={{
      display: 'flex',
      alignItems: 'center'
    }}>
        <Button slot="previous">&lt;</Button>
        <Heading style={{
        flex: 1,
        textAlign: 'center'
      }} />
        <Button slot="next">&gt;</Button>
      </div>
      <CalendarGrid style={{
      width: '100%'
    }}>
        {date => <CalendarCell date={date} style={({
        isSelected,
        isOutsideMonth
      }) => ({
        display: isOutsideMonth ? 'none' : '',
        textAlign: 'center',
        cursor: 'default',
        background: isSelected ? 'blue' : ''
      })} />}
      </CalendarGrid>
    </RangeCalendar>
}`,...(I=(O=h.parameters)==null?void 0:O.docs)==null?void 0:I.source}}};var U,D,$;m.parameters={...m.parameters,docs:{...(U=m.parameters)==null?void 0:U.docs,source:{originalSource:`{
  render: args => <RangeCalendar style={{
    width: 500
  }} visibleDuration={{
    months: 3
  }} defaultValue={{
    start: parseDate('2025-08-04'),
    end: parseDate('2025-08-10')
  }} {...args}>
      <div style={{
      display: 'flex',
      alignItems: 'center'
    }}>
        <Button slot="previous">&lt;</Button>
        <Heading style={{
        flex: 1,
        textAlign: 'center'
      }} />
        <Button slot="next">&gt;</Button>
      </div>
      <div style={{
      display: 'flex',
      gap: 20
    }}>
        <CalendarGrid style={{
        flex: 1
      }}>
          {date => <CalendarCell date={date} style={({
          isSelected,
          isOutsideMonth
        }) => ({
          display: isOutsideMonth ? 'none' : '',
          textAlign: 'center',
          cursor: 'default',
          background: isSelected ? 'blue' : ''
        })} />}
        </CalendarGrid>
        <CalendarGrid style={{
        flex: 1
      }} offset={{
        months: 1
      }}>
          {date => <CalendarCell date={date} style={({
          isSelected,
          isOutsideMonth
        }) => ({
          display: isOutsideMonth ? 'none' : '',
          textAlign: 'center',
          cursor: 'default',
          background: isSelected ? 'blue' : ''
        })} />}
        </CalendarGrid>
        <CalendarGrid style={{
        flex: 1
      }} offset={{
        months: 2
      }}>
          {date => <CalendarCell date={date} style={({
          isSelected,
          isOutsideMonth
        }) => ({
          display: isOutsideMonth ? 'none' : '',
          textAlign: 'center',
          cursor: 'default',
          background: isSelected ? 'blue' : ''
        })} />}
        </CalendarGrid>
      </div>
    </RangeCalendar>,
  args: {
    selectionAlignment: 'center'
  },
  argTypes: {
    selectionAlignment: {
      control: 'select',
      options: ['start', 'center', 'end']
    }
  }
}`,...($=(D=m.parameters)==null?void 0:D.docs)==null?void 0:$.source}}};const Z=["CalendarExample","CalendarResetValue","CalendarMultiMonth","CalendarFirstDayOfWeekExample","RangeCalendarExample","RangeCalendarMultiMonthExample"];export{g as CalendarExample,f as CalendarFirstDayOfWeekExample,y as CalendarMultiMonth,p as CalendarResetValue,h as RangeCalendarExample,m as RangeCalendarMultiMonthExample,Z as __namedExportsOrder,Y as default};
