import React from "react";
import UsergroupList from "../UsergroupList.jsx";
import { shallow } from "enzyme";
import Enzyme from "enzyme";
import Adapter from "enzyme-adapter-react-16";

Enzyme.configure({ adapter: new Adapter() });

describe("Snapshot test", () => {
  beforeEach(() => {
    window.fetch = jest.fn(link => {
      if (link.includes("getToken")) {
        return Promise.resolve({
          status: 200,
          json: () =>
            Promise.resolve({
              data: {
                getToken: "randomString2"
              }
            })
        });
      } else if (
        link.includes(
          '/api/?query={getUsergroups(access_token:"randomString2")}'
        )
      ) {
        return Promise.resolve({
          status: 200,
          json: () =>
            Promise.resolve({
              data: {
                getUsergroups:
                  '[{"idusergroup":1,"name":"grupa"}, {"idusergroup":2,"name":"grupa42"}]'
              }
            })
        });
      }
    });
  });

  it("renders as expected", () => {
    const wrapper = shallow(<UsergroupList />);
    wrapper.setState({
      usergroups: ["Grupa pierwsza", "2E"]
    });
    expect(wrapper).toMatchSnapshot();
  });
});
