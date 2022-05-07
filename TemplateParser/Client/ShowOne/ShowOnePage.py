import os
from TemplateParser.TemplateParser import TemplateParser
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
    in_file = "./show_one_page.js"
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
            in_file="./one_to_many_display.txt",
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
            in_file="./add_drop_many.txt",
            many_model=many_model,
            alias=alias,
          )
          self.out_lines = self.out_lines + insert

      elif "$$MANY_TO_MANY:2" in line:
        pass

      else:
        self.out_lines.append(line)

      '''
      elif "$$MANY_TO_MANY" in line:
        new_l = line.split(":")
        if len(model['many_to_many']) > 0:
          n_dyn = new_l[1].strip()
          if n_dyn == "0": 
            for many in model['many_to_many']:
              """
              const [courseId, setCourseId] = useState("");
              """
              many_model = find_model(db_params, many)
              m_name = many.strip().lower()
              out_f.write(f"\tconst [{m_name}Id, set{m_name.title()}Id] = useState("");\n")

          elif n_dyn == "1": 
            for many in self.model.many_to_many:
              """
              function addCourse() {
                try {
                  axios.post(`http://localhost:8080/users/${id}/add-course/${courseId}`);
                  axios.post(`http://localhost:8080/courses/${courseId}/add-user/${id}`);
                } catch (e) {
                  console.log(e);
                };
                window.location.reload();
              }

              function dropCourse(droppedId) {
                try {
                  axios.post(`http://localhost:8080/users/${id}/drop-course/${droppedId}`);
                  axios.post(`http://localhost:8080/courses/${droppedId}/drop-user/${id}`);
                } catch (e) {
                  console.log(e);
                };
                window.location.reload();
              }
              """
              many_model = find_model(db_params, many)
              sub_in_f = open("../../../../../templates/client/add_drop_many.txt", "r")
              add_snip_dynamic(sub_in_f, out_f, model, many_model, link=link, auth_object=auth_object)
              sub_in_f.close()

          elif n_dyn == "2": 
            if styled:
              for many in model['many_to_many']:
                """
                <div className='displayContainer'>

                  <h3>Courses</h3>
                  <div className='row'>

                    <TextField
                      label="course id" size="small" style={{marginRight: 10}}
                      onChange={(e) => { setCourseId(e.target.value) }}
                    />
                    <Button variant={'contained'} onClick={addCourse}>Add Course</Button>

                  </div>
                  <ul>
                  {user.courses && user.courses.map((course, i) => (
                    <div className="listItem" key={i}>
                      <li>{course.name}</li>

                      <ButtonGroup variant="outlined" size="small">
                        <Button onClick={() => navigate(`/courses/${course._id}`)}>show</Button>
                        <Button color="error" onClick={() => dropCourse(course._id)}>drop</Button>
                      </ButtonGroup>

                    </div>
                  ))}
                  </ul>

                </div>
                """
                many_model = find_model(db_params, many)
                m_name = many.strip().lower()

                out_f.write(f"\n\t\t\t\t<div className='displayContainer'>\n")

                out_f.write(f"\t\t\t\t\t<h3>{m_name.title()}s</h3>\n")

                out_f.write(f"\t\t\t\t\t<div className='row'>\n")

                out_f.write(f"\t\t\t\t\t\t<TextField\n")
                out_f.write(f"\t\t\t\t\t\t\tlabel='{m_name} id' size='small' style={{{{marginRight: 10}}}}\n")
                out_f.write(f"\t\t\t\t\t\t\tonChange={{(e) => {{ set{m_name.title()}Id(e.target.value) }}}}\n")
                out_f.write(f"\t\t\t\t\t\t/>\n")
                out_f.write(f"\t\t\t\t\t\t<Button variant='contained' onClick={{add{m_name.title()}}}>Add {m_name.title()}</Button>\n")

                out_f.write(f"\t\t\t\t\t</div>\n")

                out_f.write(f"\t\t\t\t\t<ul>\n")
                out_f.write(f"\t\t\t\t\t{{{name.lower()}.{m_name}s && {name.lower()}.{m_name}s.map(({m_name}, i) => (\n")
                out_f.write(f"\t\t\t\t\t\t<div className='listItem' key={{i}}>\n")
                out_f.write(f"\t\t\t\t\t\t\t<li>{{{m_name}.{many_model['schema'][0]['name']}}}</li>\n")

                out_f.write(f"\t\t\t\t\t\t\t<ButtonGroup variant='outlined' size='small'>\n")
                out_f.write(f"\t\t\t\t\t\t\t\t<Button onClick={{() => navigate(`/{m_name}s/${{{m_name}._id}}`)}}>show</Button>\n")
                out_f.write(f"\t\t\t\t\t\t\t\t<Button color='error' onClick={{() => drop{m_name.title()}({m_name}._id)}}>drop</Button>\n")
                out_f.write(f"\t\t\t\t\t\t\t</ButtonGroup>\n")
  
                out_f.write(f"\t\t\t\t\t\t</div>\n")
                out_f.write(f"\t\t\t\t\t))}}\n")
                out_f.write(f"\t\t\t\t\t</ul>\n")

                out_f.write(f"\t\t\t\t</div>\n")

            else:
              for many in model['many_to_many']:
                """
                <h3>Courses</h3>
                <div className='row'>
                  <input type='String' 
                    onChange={(e) => { setCourseId(e.target.value) }}
                  />
                  <button onClick={addCourse}>Add Course</button>
                </div>
                <ul>
                {user.courses && user.courses.map((course, i) => (
                  <div className="listItem" key={i}>
                    <li>{course.name}</li>
                    <Link to={`/posts/${post._id}`}>
                      <button className="listButton">show</button>
                    </Link>
                    <button className="listButton" onClick={() => dropCourse(course._id)}>drop</button>
                  </div>
                ))}
                </ul>
                """
                many_model = find_model(db_params, many)
                m_name = many.strip().lower()
                out_f.write(f"\n\t\t\t\t<h3>{m_name.title()}s</h3>\n")

                out_f.write(f"\t\t\t\t<div className='row'>\n")
                out_f.write(f"\t\t\t\t\t<input type='String'\n")
                out_f.write(f"\t\t\t\t\t\tonChange={{(e) => {{ set{m_name.title()}Id(e.target.value) }}}}\n")
                out_f.write(f"\t\t\t\t\t/>\n")
                out_f.write(f"\t\t\t\t\t<button onClick={{add{m_name.title()}}}>Add {m_name.title()}</button>\n")
                out_f.write(f"\t\t\t\t</div>\n")

                out_f.write(f"\t\t\t\t<ul>\n")
                out_f.write(f"\t\t\t\t{{{name.lower()}.{m_name}s && {name.lower()}.{m_name}s.map(({m_name}, i) => (\n")
                out_f.write(f"\t\t\t\t\t<div className='listItem' key={{i}}>\n")
                out_f.write(f"\t\t\t\t\t\t<li>{{{m_name}.{many_model['schema'][0]['name']}}}</li>\n")
                out_f.write(f"\t\t\t\t\t\t<Link to={{`/{m_name}s/${{{m_name}._id}}`}}>\n")
                out_f.write(f"\t\t\t\t\t\t\t<button className='listButton'>show</button>\n")
                out_f.write(f"\t\t\t\t\t\t</Link>\n")
                out_f.write(f"\t\t\t\t\t\t<button className='listButton' onClick={{() => drop{m_name.title()}({m_name}._id)}}>drop</button>\n")
                out_f.write(f"\t\t\t\t\t</div>\n")
                out_f.write(f"\t\t\t\t))}}\n")
                out_f.write(f"\t\t\t\t</ul>\n")
      
      elif "$$AUTH" in line:
        new_l = line.split(":")
        n_dyn = new_l[1].strip()
        if n_dyn == "0" and auth_object:
          out_f.write("import authHeader from '../../services/auth-header';\n")
      
      else:
        # INSERT VARS 
        dyn = insert_dynamic(line, out_f, model, link, port, auth_object=auth_object)
        if (not dyn):
          line = line.strip().split(":")
          if len(line) > 1:
            n_dyn = int(line[1])

            # DYNAMIC INSERTS
            if n_dyn == 0:
              for param in model['schema']:
                p_name = param["name"]
                p_type = param["type"]
                if p_type == "Boolean":
                  out_f.write(f"\t\t\t\t<label>{p_name.title()}: {{{name.lower()}.{p_name}  ? 'true' : 'false'}}</label>\n")
                elif p_type == "mongoose.Schema.Types.ObjectId":
                  out_f.write(f"\t\t\t\t<label>{p_name.title()}: <Link to={{`/{p_name}s/${{{name.lower()}.{p_name}}}`}}>{{{name.lower()}.{p_name}}}</Link></label>\n")
                else:
                  out_f.write(f"\t\t\t\t<label>{p_name.title()}: {{{name.lower()}.{p_name}}}</label>\n")

      '''
        