import React from "react";
import Notatki from "../Notatki.jsx";
import { shallow } from "enzyme";
import Enzyme from "enzyme";
import Adapter from "enzyme-adapter-react-16";

Enzyme.configure({ adapter: new Adapter() });

describe("Snapshot test", () => {
  beforeEach(() => {
    window.fetch = jest.fn(link => {
      if (link.includes("/api/?query={getUsergroups")) {
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
      } else {
        return Promise.resolve({
          status: 200,
          json: () =>
            Promise.resolve({
              data: {
                getToken: "randomString"
              }
            })
        });
      }
    });
  });

  it("renders as expected", () => {
    const wrapper = shallow(<Notatki />);
    expect(wrapper.instance().preDeleteNote(2));
  });

  it("renders as expectedd", () => {
    const wrapper = shallow(<Notatki />);
    expect(
      wrapper
        .instance()
        .preDeleteNote({
          target: { parentElement: { previousSibling: { id: "note3" } } }
        })
    );
  });
});
