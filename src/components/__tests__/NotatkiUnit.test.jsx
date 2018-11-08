import React from 'react';
import Notatki from '../Notatki.jsx';
import { shallow } from 'enzyme';
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

Enzyme.configure({ adapter: new Adapter() });

describe('Snapshot test', () => {
    beforeEach(() => {
        window.fetch = jest.fn((link) => {
            if (link.includes('/api?query={getUsergroups')) {
                return Promise.resolve({
                    status: 200,
                    json: () => Promise.resolve({
                        "data": {
                            "getUsergroups": '[{"idusergroup":1,"name":"grupa"}, {"idusergroup":2,"name":"grupa42"}]'
                        },
                    })
                })
            } else {
                return Promise.resolve({
                    status: 200,
                    json: () => Promise.resolve({
                        "data": {
                            "getToken": 'randomString'
                        },
                    })
                })
            }
        })
    })


    const wrapper = shallow(<Notatki />);
    it('PreDeleteNote finds id correctly when direct', () => {
        expect(wrapper.instance().preDeleteNote(2)).toEqual(2);
    })

    it('PreDeleteNote finds id correctly when event.target', () => {
        expect(wrapper.instance().preDeleteNote({ "target":{"parentElement":{"previousSibling":{"id":"note3"}}}})).toBe(3);
    })
    it('PreDeleteFolder finds id correctly when direct', () => {
        expect(wrapper.instance().preDeleteFolder(2)).toEqual(2);
    })

    it('PreDeleteFolder finds id correctly when event.target', () => {
        expect(wrapper.instance().preDeleteFolder({ "target":{"parentElement":{"previousSibling":{"id":"3"}}}})).toBe(3);
    })
})