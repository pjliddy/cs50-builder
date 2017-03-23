from helpers import *

def get_content( id, vars ):  
  if id == 'home':
    
    return("<h1>Welcome, " + vars['username'] + ":</h1>" + 
           "<p class='lead'>This is default content.</p>" + 
           "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce in tortor non erat auctor venenatis. Duis eu urna ac enim ullamcorper porta. Suspendisse sagittis nisl sem, id elementum arcu volutpat imperdiet. Integer tellus turpis, fermentum ut nisl eu, consectetur eleifend tellus. Aliquam erat volutpat. Nam a leo eget urna efficitur posuere. Morbi eget ullamcorper lorem. In in vulputate lorem. Nam suscipit, quam et mollis tincidunt, diam sapien porttitor risus, vel tristique turpis sapien et metus.</p>")
  elif id == 'core':
    return("<h1>CORE Heading Level 1 <small class='muted'>with muted small text</small></h1>" + 
           
           "<p class='lead'><strong>Lead Paragraph. </strong>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce in tortor non erat auctor venenatis. Duis eu urna ac enim ullamcorper porta. Suspendisse sagittis nisl sem, id elementum arcu volutpat imperdiet. Integer tellus turpis, fermentum ut nisl eu, consectetur eleifend tellus. Aliquam erat volutpat. Nam a leo eget urna efficitur posuere. Morbi eget ullamcorper lorem. In in vulputate lorem. Nam suscipit, quam et mollis tincidunt, diam sapien porttitor risus, vel tristique turpis sapien et metus.</p>" +

           "<h2>Heading Level 2 <small class='muted'>with muted small text</small></h2>" +
           
           "<p><strong>Paragraph. </strong>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce in tortor non erat auctor venenatis. Duis eu urna ac enim ullamcorper porta. Suspendisse sagittis nisl sem, id elementum arcu volutpat imperdiet. Integer tellus turpis, fermentum ut nisl eu, consectetur eleifend tellus. Aliquam erat volutpat. Nam a leo eget urna efficitur posuere. Morbi eget ullamcorper lorem. In in vulputate lorem. Nam suscipit, quam et mollis tincidunt, diam sapien porttitor risus, vel tristique turpis sapien et metus.</p>" + 

           "<h3>Heading Level 3 <small class='muted'>with muted small text</small></h3>" + 
           
           "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce in tortor non erat auctor venenatis. Duis eu urna ac enim ullamcorper porta. Suspendisse sagittis nisl sem, id elementum arcu volutpat imperdiet. Integer tellus turpis, fermentum ut nisl eu, consectetur eleifend tellus. Aliquam erat volutpat. Nam a leo eget urna efficitur posuere. Morbi eget ullamcorper lorem. In in vulputate lorem. Nam suscipit, quam et mollis tincidunt, diam sapien porttitor risus, vel tristique turpis sapien et metus.</p>" +

           "<h4>Heading Level 4 <small class='muted'>with muted small text</small></h4>" +
           
           "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce in tortor non erat auctor venenatis. Duis eu urna ac enim ullamcorper porta. Suspendisse sagittis nisl sem, id elementum arcu volutpat imperdiet. Integer tellus turpis, fermentum ut nisl eu, consectetur eleifend tellus. Aliquam erat volutpat. Nam a leo eget urna efficitur posuere. Morbi eget ullamcorper lorem. In in vulputate lorem. Nam suscipit, quam et mollis tincidunt, diam sapien porttitor risus, vel tristique turpis sapien et metus. Mauris pulvinar, libero vitae ultricies dictum, justo justo tristique metus, quis tincidunt dolor orci in sem. Quisque id lacus sit amet ex faucibus ultricies ac ac urna. Nulla vel erat lacus.</p>" +

           "<h5>Heading Level 5 <small class='muted'>with muted small text</small></h5>" +
           
           "<p>Vivamus non porttitor augue. Cras molestie nunc ante, sed condimentum massa pretium id. Vestibulum et dolor non justo tristique sodales in varius velit. Praesent nec dignissim ligula. Pellentesque non urna in nunc porta pellentesque eu sed tellus. Suspendisse molestie nunc at suscipit imperdiet. Etiam ut tincidunt purus. Proin maximus, lacus a iaculis aliquam, quam lectus fermentum ante, in dignissim arcu dui eu nulla. Sed sit amet accumsan tortor, sit amet efficitur ipsum.</p>" +

           "<h6>Heading Level 6 <small class='muted'>with muted small text</small></h6>" +
           
           "<p class='small'><strong>Small Paragraph. </strong>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce in tortor non erat auctor venenatis. Duis eu urna ac enim ullamcorper porta. Suspendisse sagittis nisl sem, id elementum arcu volutpat imperdiet. Integer tellus turpis, fermentum ut nisl eu, consectetur eleifend tellus. Aliquam erat volutpat. Nam a leo eget urna efficitur posuere. Morbi eget ullamcorper lorem. In in vulputate lorem. Nam suscipit, quam et mollis tincidunt, diam sapien porttitor risus, vel tristique turpis sapien et metus. Mauris pulvinar, libero vitae ultricies dictum, justo justo tristique metus, quis tincidunt dolor orci in sem. Quisque id lacus sit amet ex faucibus ultricies ac ac urna. Nulla vel erat lacus.</p>")
  else:
    return("<h3>This is default content</h3>" + 
           
           "<p class='lead'>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce in tortor non erat auctor venenatis. Duis eu urna ac enim ullamcorper porta. Suspendisse sagittis nisl sem, id elementum arcu volutpat imperdiet. Integer tellus turpis, fermentum ut nisl eu, consectetur eleifend tellus. Aliquam erat volutpat. Nam a leo eget urna efficitur posuere. Morbi eget ullamcorper lorem. In in vulputate lorem. Nam suscipit, quam et mollis tincidunt, diam sapien porttitor risus, vel tristique turpis sapien et metus.</p>")
