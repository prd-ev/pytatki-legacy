import React from 'react';
import renderer from 'react-test-renderer';
import UsergroupList from '../UsergroupList.jsx';

describe('Snapshot test', () => {
    it('renders as expected', () => {
        const tree = renderer.create(<UsergroupList />)
            .toJSON();
        expect(tree).toMatchSnapshot();
    })
})