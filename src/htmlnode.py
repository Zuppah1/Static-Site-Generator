class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        
        return result
    
    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        
        if self.tag is None:
            return self.value
        
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
        if self.props is not None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, "", children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("missing tag")
        
        if self.children is None:
            raise ValueError("missing children")
        
        string = f"<{self.tag}>"

        for child in self.children:
           string += child.to_html()
        
        string = string + f"</{self.tag}>"

        return string


        

        
