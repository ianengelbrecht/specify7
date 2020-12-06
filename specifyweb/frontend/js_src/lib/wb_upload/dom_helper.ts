/*
*
* Various helper methods for finding DOM elements and interacting with them
*
* */

class dom_helper {


	// FIELDS

	/* Get all lines or line element containers in a container of lines */
	public static get_lines(
		container :HTMLElement,  // a container for all of the lines
		return_line_elements :boolean = false  // whether to return line elements or line element container elements
	) :HTMLElement[] /* list of line elements or line element container elements depending on return_line_elements*/ {

		const lines = Object.values(container.children);

		if (return_line_elements)
			return lines.map(line => dom_helper.get_line_elements_container(line as HTMLElement));
		else
			return lines as HTMLElement[];

	};

	/* Returns a line elements container */
	public static readonly get_line_elements_container = (
		element :HTMLElement  // either a line element or a custom select element
	) :HTMLElement /* line elements container */ => (
		(element.tagName === 'DIV' ?
			element.getElementsByClassName('wbplanview_mappings_line_elements')[0] :
			element.parentElement)) as HTMLElement;

	/* Get children of line elements container */
	public static readonly get_line_elements = (
		line_elements_container :HTMLElement  // an elements whose children would be returned
	) :HTMLElement[] /* list of line_elements_container children */ => (
		Object.values(line_elements_container.children)) as HTMLElement[];

	/* Get header element from the line element */
	public static readonly get_line_header_element = (
		line :HTMLElement  // the line element
	) :HTMLElement /* header element */ => (
		line.getElementsByClassName('wbplanview_mappings_line_header')[0]) as HTMLElement;

	/* Get header name (for headers) or textarea value (for static headers) */
	public static readonly get_line_header_name = (
		wbplanview_mappings_line_header :HTMLElement  // header element
	) :string /* header name (for headers) or textarea value (for static headers) */ => (
		wbplanview_mappings_line_header.children.length === 0 ?
			wbplanview_mappings_line_header.innerText :
			(wbplanview_mappings_line_header.children[0] as HTMLTextAreaElement).value);  // get textarea's value (for static fields)

	/* Get the mapping type for a line (`existing_header`/`new_column`/`new_static_column`) */
	public static readonly get_line_mapping_type = (
		wbplanview_mappings_line_header :HTMLElement  // header element
	) :string | null /* the mapping type for a line */ => (
		wbplanview_mappings_line_header.getAttribute('data-mapping_type'));


	// MISC

	/* Returns whether an element has a next element sibling */
	public static readonly has_next_sibling = (
		element :HTMLElement  // an element to test
	)/*boolean*/ /* whether the next element sibling exists */ =>
		element.nextElementSibling !== null;

	/* Remove all elements to the right of a specified element */
	public static remove_elements_to_the_right(
		element :HTMLElement  // the element whose siblings to the right would be removed
	) :boolean /* whether any elements were removed */ {

		let changes_made = dom_helper.has_next_sibling(element);

		while (dom_helper.has_next_sibling(element))  // @ts-ignore
			element.nextElementSibling.remove();

		return changes_made;

	};

}

export = dom_helper;