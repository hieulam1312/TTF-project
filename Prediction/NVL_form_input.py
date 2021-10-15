import streamlit as st
if 'count' not in st.session_state:
    st.session_state.count = 0
list=['D','R','D']
r=st.columns(5)
for i,col in enumerate(r):
        with col:
            if i<=2:
                b=st.text_input(list[i],key=i)
            if i==3:
                sum=0
                # with col
                if st.button('\n+ 1\n'):
                    st.session_state.count += 1
                if st.button('- 1'):
                    st.session_state.count -= 1

            if i==4:
                st.write("Counts:",st.session_state.count)
                st.write('Q.')