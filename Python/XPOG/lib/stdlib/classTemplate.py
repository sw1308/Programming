class ${elementName}(${typedBy}):
    """
        $annotation
    """
    self.TAG = '${elementTag}'
    def __init__(self${args}):
        super(${elementName}, self).__init__(${parentArgs})
${typeChecks}
${dataInstantiation}

    def __str__(self):
        return self.el(
            TAG='${elementTag}',
            content=${elementData},
            attribs=${elementAttribs}
        )
