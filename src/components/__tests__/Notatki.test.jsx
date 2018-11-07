import React from 'react';
import renderer from 'react-test-renderer';
import UsergroupList from '../UsergroupList.jsx';

describe('Snapshot test', () => {
    beforeEach(() => {
        window.fetch = jest.fn((link) => {
            if (link.includes('getToken')) {
                return Promise.resolve({
                    status: 200,
                    json: () => Promise.resolve({
                        "data": {
                            "getToken": "randomString2"
                        },
                    })
                })
            } else if (link.includes('/api?query={getUsergroups(access_token:"randomString2")}')) {
                return Promise.resolve({
                    status: 200,
                    json: () => Promise.resolve({
                        "data": {
                            "getUsergroups": '[{"idusergroup":1,"name":"grupa"}, {"idusergroup":2,"name":"grupa42"}]'
                        },
                    })
                })
            }
        })
    })

    it('renders as expected', () => {
        const tree = renderer.create(<UsergroupList />)
            .toJSON();
        setTimeout(1000);
        expect(tree).toMatchSnapshot();
    })
})