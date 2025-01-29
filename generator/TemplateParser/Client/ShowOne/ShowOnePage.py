import os
from generator.TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index, camel_case, pascal_case, singularize

class ShowOnePage(TemplateParser):
  def __init__(
      self,
      project : Project,
      model : Model,
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "show_one_page.js.enp"
    out_file = f"./{model.name}Show.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
      model
    )

    self.parse_file()

  def parse_file(self):
    for line in self.lines:

      if "$$AUTH_IMPORTS$$" in line and self.project.auth_object:
        self.out_lines.append("import authHeader from '../../services/auth-header';\n")

      if "$$ONE_TO_MANY:ONE" in line:
        for many_model, alias in self.model.one_to_many:
          """
          <h3>Posts</h3>
          <Link to={`/users/${id}/posts/new`}>
            <button>New Post</button>  
          </Link>
          <ul>
          {user.posts && user.posts.map((post, i) => (
            <div className="listItem" key={i}>
              <li>{post.title}</li>
              <Link to={`/posts/${post._id}`}>
                <button className="listButton">show</button>
              </Link>
            </div>
          ))}
          </ul>
          """
          tabs = '\t\t\t\t'
          m_name = many_model.name
          # insert = [
          #   f"{tabs}<h3>{many_model.plural}</h3>\n",
          #   f"{tabs}<Link to={{`/{self.model.name.lower()}/${{id}}/{many_model.plural.lower()}/new`}}>\n",
          #   f"{tabs}\t<button>New {many_model.name}</button>\n",
          #   f"{tabs}</Link>\n",
          #   f"{tabs}<ul>\n",
          #   f"{tabs}{{{self.model.name.lower()}.{camel_case(many_model.plural)} && {self.model.name.lower()}.{m_name}s.map(({m_name}, i) => (\n",
          #   f"{tabs}\t<div className='listItem' key={{i}}>\n",
          #   f"{tabs}\t\t<li>{{{camel_case(m_name)}.{many_model.schema[0]['name']}}}</li>\n",
          #   f"{tabs}\t\t<Link to={{`/{many_model.plural}/${{{camel_case(m_name)}._id}}`}}>\n",
          #   f"{tabs}\t\t\t<button className='listButton'>show</button>\n",
          #   f"{tabs}\t\t</Link>\n",
          #   f"{tabs}\t</div>\n",
          #   f"{tabs}))}}\n",
          #   f"{tabs}</ul>\n"
          # ]
          custom_replacement = [
            ("$$FIRST_PARAM$$", many_model.schema[0]['name'])
          ]
          insert = self.add_snip_dynamic(
            in_file="one_to_many_display.txt",
            many_model=many_model,
            alias=alias,
            custom_replacement=custom_replacement
          )
          self.out_lines = self.out_lines + insert
          
      elif "$$MANY_TO_MANY:0" in line:
        for many_model, alias in self.model.many_to_many:
          """
          const [courseId, setCourseId] = useState("");
          """
          m_name = many_model.name
          single_alias = singularize(alias)
          self.out_lines.append(f"\tconst [{camel_case(single_alias)}Id, set{pascal_case(single_alias)}Id] = useState("");\n")

      elif "$$MANY_TO_MANY:1" in line:
        for many_model, alias in self.model.many_to_many:
          # custom_replacement = [
          #   ("$$SingleManyAlias$$", singularize(pascal_case(alias))),
          #   ("$$singlemanyalias$$", singularize(alias.lower())),
          # ]
          insert = self.add_snip_dynamic(
            in_file="add_drop_many.txt",
            many_model=many_model,
            alias=alias,
          )
          self.out_lines = self.out_lines + insert

      elif "$$MANY_TO_MANY:2" in line:
        pass

      else:
        self.out_lines.append(line)
